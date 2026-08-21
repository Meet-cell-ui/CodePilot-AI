def generate_report(
    project_name,
    project_structure,
    code_analysis,
    quality_score,
    security_result
):
    """
    Generate a complete CodePilot AI analysis report.
    """

    report = f"""
========================================
          CODEPILOT AI REPORT
========================================

Project Name : {project_name}

----------------------------------------
PROJECT STRUCTURE
----------------------------------------

Project Type :
{project_structure.get("project_type", "Unknown")}

Total Files :
{project_structure.get("total_files", 0)}

Total Folders :
{project_structure.get("total_folders", 0)}

----------------------------------------
CODE ANALYSIS
----------------------------------------

Languages :
{", ".join(code_analysis.get("languages", {}).keys())}

Files Analyzed :
{code_analysis.get("files_analyzed", 0)}

Functions :
{code_analysis.get("functions", 0)}

Classes :
{code_analysis.get("classes", 0)}

----------------------------------------
QUALITY SCORE
----------------------------------------

Overall Score :
{quality_score.get("overall_score", 0)} / 100

Rating :
{quality_score.get("rating", "Unknown")}

----------------------------------------
SECURITY ANALYSIS
----------------------------------------

Security Issues Found :
{security_result.get("total_issues", 0)}

"""

    # ----------------------------------------
    # SECURITY ISSUES
    # ----------------------------------------

    issues = security_result.get("issues", [])

    if issues:

        report += "\nDetected Security Issues:\n"
        report += "----------------------------------------\n"

        for issue in issues:

            severity = issue.get("severity", "Unknown")
            issue_name = issue.get("issue", "Unknown issue")
            file_name = issue.get("file", "Unknown file")
            line = issue.get("line", "Unknown")

            report += (
                f"\n[{severity.upper()}] "
                f"{issue_name} "
                f"({file_name} : Line {line})"
            )

    else:

        report += "\nNo security issues detected.\n"

    # ----------------------------------------
    # END REPORT
    # ----------------------------------------

    report += """

========================================
        END OF CODEPILOT REPORT
========================================
"""

    return report
