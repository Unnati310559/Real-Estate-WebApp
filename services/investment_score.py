def calculate_investment_score(roi, irr, risk_level):

    score = 0

    # ROI weight
    if roi >= 15:
        score += 40
    elif roi >= 10:
        score += 30
    elif roi >= 5:
        score += 20
    else:
        score += 10


    # IRR weight
    if irr >= 12:
        score += 30
    elif irr >= 8:
        score += 20
    elif irr >= 5:
        score += 10


    # Risk weight
    if risk_level == "Low":
        score += 30
    elif risk_level == "Medium":
        score += 20
    else:
        score += 10


    return score