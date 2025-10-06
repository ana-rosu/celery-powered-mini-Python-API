from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.tasks import compute_pi
from app.enums import APIState, CeleryState

router = APIRouter()

class CalculatePiResponse(BaseModel):
    task_id: str

class CheckProgressResponse(BaseModel):
    state: APIState
    progress: float
    result: str | None

@router.get("/calculate_pi", response_model=CalculatePiResponse)
def calculate_pi_endpoint(n: int = Query(..., ge=0, description="Number of decimal digits to calculate:")):
    """Starts asynchronous Celery task to compute π (pi)."""
    task = compute_pi.delay(n)
    return CalculatePiResponse(task_id=task.id)

@router.get("/check_progress", response_model=CheckProgressResponse)
def check_progress(task_id: str = Query(..., min_length=36, max_length=36, description="Celery task ID:")):
    """Check progress and result of a given Celery task."""
    task = compute_pi.AsyncResult(task_id)
    info = task.info or {}

    if task.state == CeleryState.PENDING:
        return CheckProgressResponse(state=APIState.PROGRESS, progress=0.0, result=None)
    
    if task.state == CeleryState.PROGRESS:
        return CheckProgressResponse(
            state=APIState.PROGRESS,
            progress=info.get("progress", 0.0),
            result=info.get("result"))
    
    if task.state == CeleryState.SUCCESS:
        return CheckProgressResponse(
            state=APIState.FINISHED,
            progress=info.get("progress", 1.0),
            result=info.get("result"),
        )
    raise HTTPException(status_code=500, detail=f"Unexpected task state: {task.state}")