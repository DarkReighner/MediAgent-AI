from ollama import chat
import json

def extract_patient_info(patient_note: str):
    response = chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": f"""
Extract the following from this patient note and return ONLY valid JSON:

{{
  "age": number or null,
  "diagnosis": string or null,
  "failed_medications_count": number or null,
  "neurologist_recommendation": true or false or null
}}

Patient note:
{patient_note}
"""
            }
        ],
    )

    text = response.message.content.strip()
    return json.loads(text)