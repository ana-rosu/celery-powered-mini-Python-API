from enum import Enum

class APIState(str, Enum):
    """API response states."""
    PROGRESS = "PROGRESS"
    FINISHED = "FINISHED"

class CeleryState(str, Enum):
    """Celery internal task states."""
    PENDING = "PENDING"
    PROGRESS = "PROGRESS"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"