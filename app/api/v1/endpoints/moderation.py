from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from app.services.moderation_service import ModerationService
from app.api.v1.models import ModerationRequest, ModerationResponse
from app.tasks.moderation_tasks import process_moderation_task

router = APIRouter()

@router.post("/text", response_model=ModerationResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def moderate_text(request: ModerationRequest):
    try:
        # Enqueue the task for async processing
        task = process_moderation_task.delay(request.text)
        return {"task_id": task.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))