from fastapi import APIRouter, HTTPException, Request, Query, Header
from pydantic import BaseModel
from app.storage import result_store
import requests
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

log_handler = RotatingFileHandler(
    "analyze_calls.log",     # nom du fichier
    maxBytes=5 * 1024 * 1024, # 5 Mo
    backupCount=5             # nombre max de fichiers conservés
)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("analyze_logger")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

router = APIRouter()
API_SECRET = os.environ.get("API_SECRET")

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
def analyze_transcript(
    req: AnalysisRequest,
    x_api_key: str = Header(default="anonymous"),
    request: Request = None
):
    log_entry = (
        f"API call to /analyze | IP={request.client.host} | "
        f"API_KEY={x_api_key} | VIDEO_ID={req.video_id} | "
        f"Transcript[60]={req.transcript[:60].replace(chr(10), ' ')}..."
    )
    logger.info(log_entry)

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
async def receive_result(video_id: str, request: Request, x_api_key: str = Header(...)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        body = await request.json()
    except Exception as e:
        print("[ERREUR JSON]", e)
        body_raw = await request.body()
        print("[CORPS REÇU]", body_raw.decode())
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    print("[✅ BODY VALIDE]", body)
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
def get_result(video_id: str, x_api_key: str = Header(...)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print("📦 result_store:", result_store)
    result = result_store.get(video_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not ready or video_id not found.")
    return result