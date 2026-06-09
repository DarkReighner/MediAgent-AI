def make_decision(patient_data, policy_text):
    score = 0
    reasons = []

    policy = policy_text.lower()
    diagnosis = (patient_data.get("diagnosis") or "").lower()

    age = patient_data.get("age")
    failed_count = patient_data.get("failed_medications_count")
    neuro = patient_data.get("neurologist_recommendation")

    if age is not None and age >= 18:
        score += 1
        reasons.append("Age criteria met")
    else:
        reasons.append("Age criteria not met")

    if failed_count is not None and failed_count >= 2:
        score += 1
        reasons.append("Failed medication criteria met")
    else:
        reasons.append("Failed medication criteria not met")

    if neuro is True:
        score += 1
        reasons.append("Neurologist recommendation present")
    else:
        reasons.append("Neurologist recommendation missing")

    if "migraine" in diagnosis and "migraine" in policy:
        score += 1
        reasons.append("Diagnosis matches policy")
    else:
        reasons.append("Diagnosis-policy match weak")

    if score >= 4:
        decision = "APPROVED"
    elif score >= 2:
        decision = "ESCALATE"
    else:
        decision = "REJECTED"

    return {
        "decision": decision,
        "reason": ", ".join(reasons),
        "score": score
    }