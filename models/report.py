from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Category(str, Enum):
    street_damage = "street_damage"
    water_leakage = "water_leakage"
    waste_management = "waste_management"
    other_infra = "other_infra"


class ReportOut(BaseModel):
    id: str
    category: str
    image_url: str
    cloudinary_public_id: str
    address: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str
    created_at: str
