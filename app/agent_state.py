from typing import TypedDict

class MediAgentState(TypedDict):
    patient_note: str
    extracted_data: dict
    policy_text: str
    decision: dict