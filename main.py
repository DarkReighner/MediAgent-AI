from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

from app.audit import save_log
from app.pdf_reader import extract_pdf_text
from app.workflow import graph

app = FastAPI(title="MediAgent")
from app.fhir import router as fhir_router

app.include_router(fhir_router)


@app.get("/")
def home():
    return {"message": "MediAgent Running"}


@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MediAgent</title>

        <style>
            body{
                background:#f4f7fa;
                font-family:Arial;
            }

            .container{
                width:900px;
                margin:auto;
                margin-top:40px;
            }

            .card{
                background:white;
                padding:25px;
                border-radius:15px;
                box-shadow:0 2px 10px rgba(0,0,0,0.1);
                margin-bottom:20px;
            }

            input{
                width:100%;
                padding:12px;
                margin-top:5px;
                margin-bottom:15px;
                border:1px solid #ccc;
                border-radius:8px;
            }

            button{
                background:#2563eb;
                color:white;
                border:none;
                padding:12px 20px;
                border-radius:8px;
                cursor:pointer;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <div class="card">
                <h1>🏥 MediAgent</h1>
                <p>AI Powered Prior Authorization Assistant</p>
            </div>

            <div class="card">

                <h2>Manual Entry</h2>

                <form action="/analyze">

                    <label>Patient Age</label>
                    <input name="age">

                    <label>Diagnosis</label>
                    <input name="diagnosis">

                    <label>Failed Medications</label>
                    <input name="medications">

                    <label>Neurologist Recommendation</label>
                    <input name="recommendation">

                    <button type="submit">
                        Analyze Patient
                    </button>

                </form>

            </div>

            <div class="card">

                <h2>Upload Clinical Note PDF</h2>

                <form action="/upload-pdf"
                      method="post"
                      enctype="multipart/form-data">

                    <input type="file" name="file">

                    <br><br>

                    <button type="submit">
                        Analyze PDF
                    </button>

                </form>

            </div>

        </div>

    </body>
    </html>
    """


def build_dashboard(result):

    extracted = result["extracted_data"]
    decision = result["decision"]

    color = "#22c55e"
    emoji = "🟢"

    if decision["decision"] == "REJECTED":
        color = "#ef4444"
        emoji = "🔴"

    elif decision["decision"] == "ESCALATE":
        color = "#f59e0b"
        emoji = "🟡"

    confidence = min(decision["score"] * 25, 100)

    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>MediAgent Result</title>

        <style>

            body{{
                background:#f4f7fa;
                font-family:Arial;
            }}

            .container{{
                width:1000px;
                margin:auto;
                margin-top:40px;
            }}

            .card{{
                background:white;
                padding:25px;
                border-radius:15px;
                margin-bottom:20px;
                box-shadow:0 2px 10px rgba(0,0,0,0.1);
            }}

            .decision{{
                background:{color};
                color:white;
                padding:25px;
                border-radius:15px;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <div class="card">
                <h1>🏥 MediAgent Dashboard</h1>
            </div>

            <div class="card">

                <h2>Patient Summary</h2>

                <p><b>Age:</b> {extracted.get("age")}</p>

                <p><b>Diagnosis:</b> {extracted.get("diagnosis")}</p>

                <p><b>Failed Medications:</b> {extracted.get("failed_medications_count")}</p>

                <p><b>Neurologist Recommendation:</b> {extracted.get("neurologist_recommendation")}</p>

            </div>

            <div class="card">

                <h2>Retrieved Policy</h2>

                <p>{result.get("policy_text", "Policy Retrieved")}</p>

            </div>

            <div class="decision">

                <h1>{emoji} {decision["decision"]}</h1>

                <h3>Score: {decision["score"]}/4</h3>

                <h3>Confidence: {confidence}%</h3>

                <p>{decision["reason"]}</p>

            </div>

            <div class="card">

                <h2>Workflow</h2>

                <p>✅ Intake Agent</p>
                <p>✅ Extraction Agent</p>
                <p>✅ Retrieval Agent</p>
                <p>✅ Decision Agent</p>
                <p>✅ Audit Agent</p>

            </div>

            <a href="/ui">
                <button>
                    Analyze Another Patient
                </button>
            </a>

        </div>

    </body>

    </html>
    """


@app.get("/analyze", response_class=HTMLResponse)
def analyze(
    age: str,
    diagnosis: str,
    medications: str,
    recommendation: str
):

    patient_note = f"""
    Patient Age: {age}

    Diagnosis: {diagnosis}

    Failed Medications:
    {medications}

    Neurologist Recommendation:
    {recommendation}
    """

    result = graph.invoke(
        {
            "patient_note": patient_note
        }
    )

    save_log(result["decision"]["decision"])

    return build_dashboard(result)


@app.post("/upload-pdf", response_class=HTMLResponse)
async def upload_pdf(file: UploadFile = File(...)):

    contents = await file.read()

    with open("uploaded_note.pdf", "wb") as f:
        f.write(contents)

    patient_note = extract_pdf_text("uploaded_note.pdf")

    result = graph.invoke(
        {
            "patient_note": patient_note
        }
    )

    save_log(result["decision"]["decision"])

    return build_dashboard(result)


@app.get("/agent-evaluate")
def agent_evaluate():

    patient_note = '''
    Patient Age: 25
    Diagnosis: Chronic Migraine

    Failed Medications:
    Medicine A
    Medicine B

    Neurologist Recommendation:
    Yes
    '''

    result = graph.invoke(
        {
            "patient_note": patient_note
        }
    )

    save_log(result["decision"]["decision"])

    return result