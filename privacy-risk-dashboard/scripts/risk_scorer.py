def calculate_risk_score(risks):
    score = 0
    for risk in risks:
        if risk['type'] == 'High-Risk PII Detected':
            score += 10
        elif risk['type'] == 'Data Retention Violation':
            score += 15
        else:
            score += 5  # default for any unknown types

    if score >= 30:
        risk_level = "High"
    elif score >= 15:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {
        'total_score': score,
        'risk_level': risk_level,
        'total_risks': len(risks)
    }

