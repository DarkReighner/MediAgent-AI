def match_policy(patient_note, policy_text):
    note = patient_note.lower()
    policy = policy_text.lower()

    score = 0

    if "migraine" in note and "migraine" in policy:
        score += 1
    if "failed" in note and "failed" in policy:
        score += 1
    if "neurologist" in note and "neurologist" in policy:
        score += 1
    if "age" in note and "18" in policy:
        score += 1

    if score >= 3:
        decision = "APPROVED"
        reason = "Patient note matches most policy criteria."
    elif score == 2:
        decision = "ESCALATE"
        reason = "Partial match found. Human review needed."
    else:
        decision = "REJECTED"
        reason = "Not enough policy criteria matched."

    return {
        "decision": decision,
        "reason": reason,
        "match_score": score
    }