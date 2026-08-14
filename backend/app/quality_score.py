def calculate_quality_score(code_analysis, security_issues=None):

    if security_issues is None:
        security_issues = []

    score = 100

    files = code_analysis.get("files_analyzed", 0)
    functions = code_analysis.get("functions", 0)
    classes = code_analysis.get("classes", 0)
    issues = code_analysis.get("issues", [])

    # ---------------------------------
    # CODE QUALITY ISSUES
    # ---------------------------------

    score -= len(issues) * 5

    # ---------------------------------
    # FUNCTION COMPLEXITY INDICATOR
    # ---------------------------------

    if files > 0:

        avg_functions = functions / files

        if avg_functions > 20:
            score -= 10

        elif avg_functions > 10:
            score -= 5

    # ---------------------------------
    # CLASS STRUCTURE
    # ---------------------------------

    if files > 50 and classes < 5:
        score -= 10

    # ---------------------------------
    # SECURITY ISSUES
    # ---------------------------------

    for issue in security_issues:

        severity = issue.get("severity", "").lower()

        if severity == "critical":
            score -= 20

        elif severity == "high":
            score -= 15

        elif severity == "medium":
            score -= 7

        elif severity == "low":
            score -= 3

    # ---------------------------------
    # KEEP SCORE BETWEEN 0 AND 100
    # ---------------------------------

    score = max(0, min(score, 100))

    # ---------------------------------
    # RATING
    # ---------------------------------

    if score >= 90:
        rating = "Excellent"

    elif score >= 80:
        rating = "Very Good"

    elif score >= 70:
        rating = "Good"

    elif score >= 60:
        rating = "Average"

    else:
        rating = "Poor"

    return {
        "overall_score": score,
        "rating": rating
    }
