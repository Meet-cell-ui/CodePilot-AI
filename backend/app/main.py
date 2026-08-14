from fastapi import FastAPI, UploadFile, File, HTTPException, Depends

from app.analyzer import analyze_project
from app.code_analyzer import analyze_code
from app.report_generator import generate_report
from app.quality_score import calculate_quality_score
from app.security_scanner import scan_security
from app.recommendation_engine import generate_recommendations
from app.services.ai_service import generate_ai_analysis

from app.security import verify_api_key
from app.api_key_manager import create_api_key

import zipfile
import shutil
import os


app = FastAPI(
    title="CodePilot AI",
    description="AI-powered Software Engineering Platform",
    version="0.3.0"
)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "Welcome to CodePilot AI",
        "status": "Backend Running",
        "version": "0.3.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api-keys")
def create_new_api_key():
    api_key = create_api_key()

    return {
        "success": True,
        "message": "CodePilot API key created successfully.",
        "api_key": api_key
    }


@app.post("/upload")
async def upload_project(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are allowed."
        )

    try:

        # --------------------------------
        # Save uploaded ZIP
        # --------------------------------

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # --------------------------------
        # Project name
        # --------------------------------

        project_name = os.path.splitext(
            file.filename
        )[0]

        # --------------------------------
        # Extraction folder
        # --------------------------------

        extract_folder = os.path.join(
            UPLOAD_FOLDER,
            project_name
        )

        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)

        os.makedirs(extract_folder)

        # --------------------------------
        # Extract ZIP
        # --------------------------------

        with zipfile.ZipFile(
            file_path,
            "r"
        ) as zip_ref:
            zip_ref.extractall(extract_folder)

        # --------------------------------
        # Project structure analysis
        # --------------------------------

        project_structure = analyze_project(
            extract_folder
        )

        # --------------------------------
        # Code analysis
        # --------------------------------

        code_analysis = analyze_code(
            extract_folder
        )

        # --------------------------------
        # Security analysis
        # --------------------------------

        security_issues = scan_security(
            extract_folder
        )

        # --------------------------------
        # Quality score
        # --------------------------------

        quality_score = calculate_quality_score(
            code_analysis,
            security_issues
        )

        # --------------------------------
        # Recommendations
        # --------------------------------

        recommendations = generate_recommendations(
            {
                "code_analysis": code_analysis,
                "quality_score": quality_score,
                "security": {
                    "total_issues": len(security_issues),
                    "issues": security_issues
                }
            }
        )

        # --------------------------------
        # Gemini AI analysis
        # --------------------------------

        ai_analysis = generate_ai_analysis(
            {
                "project_structure": project_structure,
                "code_analysis": code_analysis,
                "quality_score": quality_score,
                "security": {
                    "total_issues": len(security_issues),
                    "issues": security_issues
                },
                "recommendations": recommendations
            }
        )

        # --------------------------------
        # Complete analysis
        # --------------------------------

        analysis = {
            "project_structure": project_structure,
            "code_analysis": code_analysis,
            "quality_score": quality_score,
            "security": {
                "total_issues": len(security_issues),
                "issues": security_issues
            },
            "recommendations": recommendations,
            "ai_analysis": ai_analysis
        }

        # --------------------------------
        # Generate report
        # --------------------------------

        report = generate_report(
            project_name,
            analysis
        )

        # --------------------------------
        # Final response
        # --------------------------------

        return {
            "success": True,
            "project_name": project_name,
            "analysis": analysis,
            "report": report
        }

    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=400,
            detail="Invalid ZIP file."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
