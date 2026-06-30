import uuid
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from database import db
from models.report import Category
from routes.auth import get_current_user
from services.cloudinary_service import upload_image

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("")
async def create_report(
    image: UploadFile = File(...),
    category: Category = Form(...),
    address: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    username: str = Depends(get_current_user),
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    file_bytes = await image.read()
    unique_name = f"{uuid.uuid4()}_{image.filename}"

    try:
        image_url, public_id = await upload_image(file_bytes, unique_name)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Image upload failed: {str(e)}")

    doc = {
        "username": username,
        "category": category.value,
        "image_url": image_url,
        "cloudinary_public_id": public_id,
        "address": address,
        "description": description,
        "latitude": latitude,
        "longitude": longitude,
        "status": "open",
    }

    report_id = await db.insert_report(doc)
    return JSONResponse(status_code=201, content={"id": report_id, **doc})


@router.get("")
async def list_reports(category: Optional[str] = None, limit: int = 20):
    reports = await db.get_reports(category=category, limit=limit)
    return [{"id": r["_id"], **{k: v for k, v in r.items() if k != "_id"}} for r in reports]


@router.get("/stats")
async def get_stats():
    return await db.get_stats()


@router.patch("/{report_id}/close")
async def close_report(report_id: str, username: str = Depends(get_current_user)):
    report = await db.close_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return {"id": report["_id"], **{k: v for k, v in report.items() if k != "_id"}}


@router.get("/leaderboard")
async def leaderboard(limit: int = 10):
    return await db.get_leaderboard(limit=limit)
