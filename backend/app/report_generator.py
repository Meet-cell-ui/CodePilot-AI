def generate_report(project_name, analysis):

    project = analysis["project_structure"]
    code = analysis["code_analysis"]
    quality = analysis["quality_score"]
    security = analysis["security"]

    report = f"""
========================================
          CODEPILOT AI REPORT
========================================

Project Name : {project_name}

Project Type : {project.get("project_type", "Unknown")}

Total Files : {project.get("total_files", 0)}
Total Folders : {project.get("total_folders", 0)}

----------------------------------------
CODE ANALYSIS
----------------------------------------

Languages :
{", ".join(code.get("languages", {}).keys())}

Files Analyzed :
{code.get("files_analyzed", 0)}

Functions :
{code.get("functions", 0)}

Classes :
{code.get("classes", 0)}

----------------------------------------
QUALITY SCORE
----------------------------------------

Overall Score :
{quality.get("overall_score", 0)} / 100

Rating :
{quality.get("rating", "Unknown")}

----------------------------------------
SECURITY
----------------------------------------

Security Issues Found :
{security.get("total_issues", 0)}

"""

    if security.get("issues"):
        report += "\nDetected Issues:\n"

        for issue in security["issues"]:
            report += (
                f"\n[{issue['severity']}] "
                f"{issue['issue']} "
                f"({issue['file']} : Line {issue['line']})"
            )

    else:
        report += "\nNo security issues detected.\n"

    return report