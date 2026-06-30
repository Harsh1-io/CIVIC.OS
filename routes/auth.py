import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from database import db

router = APIRouter(prefix="/api/auth", tags=["auth"])

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
_SECRET  = os.getenv("JWT_SECRET", "change-me-to-a-long-random-string")
_ALGO    = "HS256"
_TOKEN_DAYS = 30


# ── Request models ────────────────────────────────────────────────────────────

class AuthRequest(BaseModel):
    username: str
    password: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_token(username: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=_TOKEN_DAYS)
    return jwt.encode({"sub": username, "exp": exp}, _SECRET, algorithm=_ALGO)


async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """FastAPI dependency — raises 401 if token missing or invalid."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, _SECRET, algorithms=[_ALGO])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/signup")
async def signup(body: AuthRequest):
    if len(body.username.strip()) < 3:
        raise HTTPException(400, "Username must be at least 3 characters.")
    if len(body.password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters.")
    if await db.get_user(body.username):
        raise HTTPException(400, "Username already taken.")
    hashed = _pwd_ctx.hash(body.password)
    await db.create_user(body.username.strip(), hashed)
    token = _make_token(body.username.strip())
    return {"token": token, "username": body.username.strip()}


@router.post("/login")
async def login(body: AuthRequest):
    user = await db.get_user(body.username)
    if not user or not _pwd_ctx.verify(body.password, user["password_hash"]):
        raise HTTPException(401, "Invalid username or password.")
    token = _make_token(user["username"])
    return {"token": token, "username": user["username"]}
