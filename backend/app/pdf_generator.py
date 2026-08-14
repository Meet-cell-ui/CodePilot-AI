from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import os
import html


def create_pdf_report(project_name, analysis):

    os.makedirs("reports", exist_ok=True)

    pdf_path = f"reports/{project_name}_report.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    project = analysis["project_structure"]
    code = analysis["code_analysis"]
    quality = analysis["quality_score"]
    security = analysis["security"]
    recommendations = analysis.get("recommendations", [])

    # Title
    story.append(
        Paragraph(
            "<b>CODEPILOT AI PROJECT REPORT</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # Project Overview
    story.append(
        Paragraph("Project Overview", styles["Heading2"])
    )

    overview = [
        ["Project Name", project_name],
        ["Project Type", project["project_type"]],
        ["Total Files", str(project["total_files"])],
        ["Total Folders", str(project["total_folders"])],
        ["Health Score", f'{project["health_score"]}/100'],
        ["Grade", project["grade"]],
        ["Database", project["database"]],
        ["Package Manager", project["package_manager"]],
    ]

    table = Table(overview, colWidths=[150, 350])

    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(table)
    story.append(Spacer(1, 15))

    # Languages
    story.append(
        Paragraph("Languages & Frameworks", styles["Heading2"])
    )

    story.append(
        Paragraph(
            "<b>Languages:</b> " +
            html.escape(", ".join(project["languages"])),
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "<b>Frameworks:</b> " +
            html.escape(", ".join(project["frameworks"])),
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # Summary
    story.append(
        Paragraph("Project Summary", styles["Heading2"])
    )

    story.append(
        Paragraph(
            html.escape(project["summary"]),
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # Code Analysis
    story.append(
        Paragraph("Code Analysis", styles["Heading2"])
    )

    code_table = [
        ["Metric", "Value"],
        ["Files Analyzed", str(code["files_analyzed"])],
        ["Functions", str(code["functions"])],
        ["Classes", str(code["classes"])],
        ["Code Issues", str(len(code["issues"]))]
    ]

    table = Table(code_table, colWidths=[250, 250])

    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(table)
    story.append(Spacer(1, 15))

    # Quality
    story.append(
        Paragraph("Quality Score", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f'<b>Overall Score:</b> {quality["overall_score"]}/100',
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f'<b>Rating:</b> {html.escape(quality["rating"])}',
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # Security
    story.append(
        Paragraph("Security Analysis", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f'<b>Security Issues Found:</b> {security["total_issues"]}',
            styles["Normal"]
        )
    )

    for issue in security["issues"]:
        story.append(
            Paragraph(
                f'<b>[{html.escape(issue["severity"])}]</b> '
                f'{html.escape(issue["issue"])} '
                f'— {html.escape(issue["file"])} '
                f'(Line {issue["line"]})',
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    # Recommendations
    story.append(
        Paragraph("Recommendations", styles["Heading2"])
    )

    for rec in recommendations:
        story.append(
            Paragraph(
                "• " + html.escape(rec),
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    # AI Analysis
    ai = analysis.get("ai_analysis", {})

    story.append(
        Paragraph("AI Assessment", styles["Heading2"])
    )

    story.append(
        Paragraph(
            html.escape(ai.get("assessment", "")),
            styles["Normal"]
        )
    )

    doc.build(story)

    return pdf_path
