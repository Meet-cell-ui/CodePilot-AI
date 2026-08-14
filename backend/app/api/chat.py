from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
from app.core.config import GEMINI_API_KEY

router = APIRouter(prefix="/chat", tags=["AI Chat"])

client = genai.Client(api_key=GEMINI_API_KEY)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message
        )

        return {
            "success": True,
            "response": response.text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
