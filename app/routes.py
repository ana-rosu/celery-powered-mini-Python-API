from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/calculate_pi")
def calculate_pi_endpoint(n: int = Query(..., gt=0, description="Number of decimals")):
    """
    Start Pi calculation (placeholder for now)
    """
    return {"task_id": "placeholder-task-id"}
