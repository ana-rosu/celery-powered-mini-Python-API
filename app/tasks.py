from celery import Celery, Task
from app.enums import CeleryState
from typing import Dict, Any
from app.calculator import calculate_pi
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task(bind=True)
def compute_pi(self: Task, n: int) -> Dict[str, Any]:
    """Celery task to compute pi asynchronously with progress tracking."""
    result = None
    for progress, value in calculate_pi(n):
        self.update_state(state=CeleryState.PROGRESS.value, meta={'progress': progress, 'result': None})
        result = value
    return {'progress': 1.0, 'result': result}
