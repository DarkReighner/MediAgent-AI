from fastapi import APIRouter

router = APIRouter(prefix="/fhir")

@router.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    return {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [
            {
                "given": ["John"],
                "family": "Doe"
            }
        ]
    }

@router.get("/condition/{condition_id}")
def get_condition(condition_id: str):
    return {
        "resourceType": "Condition",
        "id": condition_id,
        "code": {
            "text": "Chronic Migraine"
        }
    }

@router.get("/medicationrequest/{request_id}")
def get_medication(request_id: str):
    return {
        "resourceType": "MedicationRequest",
        "id": request_id,
        "status": "active"
    }