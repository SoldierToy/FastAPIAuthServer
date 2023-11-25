from fastapi import FastAPI
from src.api_v1.auth.auth import router as auth_router

app = FastAPI()

app.include_router(router=auth_router, prefix="/auth/api/v1")
