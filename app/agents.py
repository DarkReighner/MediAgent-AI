from app.ai_extractor import extract_patient_info
from app.final_decision import make_decision
from app.rag import search_policy

def extraction_agent(state):

    state["extracted_data"] = extract_patient_info(
        state["patient_note"]
    )

    return state


def retrieval_agent(state):

    diagnosis = state["extracted_data"].get(
        "diagnosis",
        ""
    )

    state["policy_text"] = search_policy(
        diagnosis
    )

    return state


def decision_agent(state):

    state["decision"] = make_decision(
        state["extracted_data"],
        state["policy_text"]
    )

    return state