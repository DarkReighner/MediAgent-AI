def approve(patient):

    if "25" in patient:
        if "Medicine A" in patient and "Medicine B" in patient:
            if "Yes" in patient:
                return {
                    "decision": "APPROVED",
                    "reason": "Patient meets all policy criteria"
                }

    return {
        "decision": "REJECTED",
        "reason": "Patient does not meet policy criteria"
    }