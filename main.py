import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.auth import router as auth_router
from routes.reports import router as reports_router
from services.cloudinary_service import init_cloudinary

app = FastAPI(title="CIVIC.OS — Public Infrastructure Tracker")

init_cloudinary()

app.include_router(auth_router)
app.include_router(reports_router)

# Serve the frontend — must be last so API routes take priority
app.mount("/", StaticFiles(directory="public", html=True), name="static")
