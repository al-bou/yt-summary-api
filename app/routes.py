from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
from app.storage import result_store
import requests
import os

router = APIRouter()

# Request model for analysis
class AnalysisRequest(BaseModel):
    video_id: str
    transcript: str

# Response model from n8n
class AnalysisResult(BaseModel):
    video_id: str
    summary: str
    keywords: list[str]
    actions: list[str]

class SummaryPayload(BaseModel):
    summary: str
    keywords: list[str]
    actions: list[str]

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

# Endpoint to receive result from n8n (optional for future storage/logging)
@router.post("/result")
async def receive_result(video_id: str, request: Request):
    body = await request.json()
    summary = body.get("summary")
    keywords = body.get("keywords")
    actions = body.get("actions")

    if not all([summary, keywords, actions]):
        raise HTTPException(status_code=400, detail="Incomplete result data")

    result_store[video_id] = {
        "summary": summary,
        "keywords": keywords,
        "actions": actions
    }
    return {"status": "success"}

@router.get("/result")
def get_result(video_id: str):
    result = result_store.get(video_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not ready or video_id not found.")
    return result