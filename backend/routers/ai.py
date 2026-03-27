from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI"])

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class DescriptionRequest(BaseModel):
    product_name: str

@router.post("/describe")
def generate_description(request: DescriptionRequest):
    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=f"Write a professional 2-sentence marketing description for a product called '{request.product_name}'. Be concise and compelling."
                    )
                ]
            )
        ]

        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )

        description = ""
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=generate_content_config,
        ):
            description += chunk.text

        return {"description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))