from google import genai
from app.core.config import GEMINI_API_KEY


# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_analysis(analysis):
    """
    Generate an AI-powered technical analysis
    of the uploaded software project.
    """

    prompt = f"""
You are CodePilot AI, an AI-powered software engineering assistant.

Analyze the following software project analysis.

Project Analysis:
{analysis}

Provide a professional technical assessment.

Focus on:

1. Overall project quality
2. Code quality
3. Security concerns
4. Architecture and maintainability
5. Important improvements
6. Practical recommendations

Give clear, concise and actionable recommendations.

Do not invent information that is not present in the analysis.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
