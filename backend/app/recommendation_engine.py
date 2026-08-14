def generate_recommendations(analysis):

    recommendations = []

    code = analysis["code_analysis"]
    quality = analysis["quality_score"]
    security = analysis["security"]

    # Quality recommendations
    if quality["overall_score"] < 80:
        recommendations.append(
            "Improve overall code quality by refactoring large and complex files."
        )

    # Security recommendations
    if security["total_issues"] > 0:
        recommendations.append(
            "Fix all detected security vulnerabilities before deployment."
        )

    # Too many functions
    if code["files_analyzed"] > 0:
        avg = code["functions"] / code["files_analyzed"]

        if avg > 20:
            recommendations.append(
                "Several files contain many functions. "
                "Consider splitting responsibilities into smaller modules."
            )

    # Too few classes
    if code["files_analyzed"] > 50 and code["classes"] < 5:
        recommendations.append(
            "The project uses very few classes. "
            "Consider improving object-oriented design where appropriate."
        )

    # No issues found
    if not recommendations:
        recommendations.append(
            "Excellent project structure. Continue following clean coding practices."
        )

    return recommendations
