from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
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


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="CodePilot AI",
    description="AI-powered Software Engineering Platform",
    version="0.3.0"
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# ROUTERS
# --------------------------------------------------

app.include_router(chat_router)


# --------------------------------------------------
# UPLOAD CONFIGURATION
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Welcome to CodePilot AI",
        "status": "Backend Running",
        "version": "0.3.0"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# CREATE CODEPILOT API KEY
# --------------------------------------------------

@app.post("/api-keys")
def create_new_api_key():

    api_key = create_api_key()

    return {
        "success": True,
        "message": "CodePilot API key created successfully.",
        "api_key": api_key
    }


# --------------------------------------------------
# UPLOAD AND ANALYZE PROJECT
# --------------------------------------------------

@app.post("/upload")
async def upload_project(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):

    # --------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are allowed."
        )

    try:

        # --------------------------------------------------
        # SAVE ZIP FILE
        # --------------------------------------------------

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # --------------------------------------------------
        # PROJECT NAME
        # --------------------------------------------------

        project_name = os.path.splitext(
            file.filename
        )[0]

        # --------------------------------------------------
        # EXTRACTION DIRECTORY
        # --------------------------------------------------

        extract_path = os.path.join(
            UPLOAD_FOLDER,
            project_name
        )

        if os.path.exists(extract_path):

            shutil.rmtree(
                extract_path
            )

        os.makedirs(
            extract_path,
            exist_ok=True
        )

        # --------------------------------------------------
        # EXTRACT ZIP
        # --------------------------------------------------

        with zipfile.ZipFile(
            file_path,
            "r"
        ) as zip_ref:

            zip_ref.extractall(
                extract_path
            )

        # --------------------------------------------------
        # PROJECT STRUCTURE ANALYSIS
        # --------------------------------------------------

        project_structure = analyze_project(
            extract_path
        )

        # --------------------------------------------------
        # CODE ANALYSIS
        # --------------------------------------------------

        code_analysis = analyze_code(
            extract_path
        )

        # --------------------------------------------------
        # SECURITY SCAN
        # --------------------------------------------------

        security_issues = scan_security(
            extract_path
        )

        security_result = {
            "total_issues": len(security_issues),
            "issues": security_issues
        }

        # --------------------------------------------------
        # QUALITY SCORE
        # --------------------------------------------------

        quality_score = calculate_quality_score(
            code_analysis,
            security_issues
        )

        # --------------------------------------------------
        # COMBINED ANALYSIS
        # --------------------------------------------------

        analysis = {
            "project_structure": project_structure,
            "code_analysis": code_analysis,
            "quality_score": quality_score,
            "security": security_result
        }

        # --------------------------------------------------
        # RECOMMENDATIONS
        # --------------------------------------------------

        recommendations = generate_recommendations(
            analysis
        )

        # Add recommendations to analysis
        analysis["recommendations"] = recommendations

        # --------------------------------------------------
        # AI ANALYSIS
        # --------------------------------------------------

        ai_analysis = generate_ai_analysis(
            analysis
        )

        # --------------------------------------------------
        # REPORT
        # --------------------------------------------------

        report = generate_report(
            project_name,
            project_structure,
            code_analysis,
            quality_score,
            security_result
        )

        # --------------------------------------------------
        # FINAL RESPONSE
        # --------------------------------------------------

        return {
            "success": True,
            "project_name": project_name,

            "analysis": {
                "project_structure": project_structure,
                "code_analysis": code_analysis,
                "quality_score": quality_score,
                "security": security_result,
                "recommendations": recommendations,
                "ai_analysis": ai_analysis
            },

            "report": report
        }

    # --------------------------------------------------
    # INVALID ZIP
    # --------------------------------------------------

    except zipfile.BadZipFile:

        raise HTTPException(
            status_code=400,
            detail="Invalid ZIP file."
        )

    # --------------------------------------------------
    # GENERAL ERROR
    # --------------------------------------------------

    except Exception as e:

        print(
            "UPLOAD ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
