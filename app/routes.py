from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os

router = APIRouter()

# Request model for analysis
class AnalysisRequest(BaseModel):
    video_id: str
    transcript: str

# Endpoint to call OpenAI (via n8n webhook)
@router.post("/analyze")
def analyze_transcript(req: AnalysisRequest):
    webhook_url = os.environ.get("N8N_AI_WEBHOOK")
    if not webhook_url:
        raise HTTPException(status_code=500, detail="Webhook URL not configured.")

    try:
        response = requests.post(
            webhook_url,
            json={
                "video_id": req.video_id,
                "transcript": req.transcript
            },
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to contact n8n: {e}")
