from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Pi Calculator API", version="1.0", description="An asynchronous API for computing π (pi) using Celery and Redis.")
app.include_router(router)