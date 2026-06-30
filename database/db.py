"""
In-memory data store.
To switch to MongoDB later:
  1. Add motor to requirements.txt
  2. Replace this file with the Motor version (keep the same function signatures)
  3. No other files need to change.
"""
import random
import uuid
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, List, Optional

_reports: List[Dict] = []
_users: Dict[str, Dict] = {}   # username -> {username, password_hash}


def _make_issue_id() -> str:
    """Generate a short human-readable ID like #A3F2."""
    return '#' + ''.join(random.choices('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ', k=4))


# ── Reports ──────────────────────────────────────────────────────────────────

async def insert_report(doc: dict) -> str:
    doc["_id"]      = str(uuid.uuid4())
    doc["issue_id"] = _make_issue_id()
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    _reports.append(doc)
    return doc["_id"]


async def get_reports(category: Optional[str] = None, limit: int = 20) -> List[Dict]:
    data = _reports if not category else [r for r in _reports if r["category"] == category]
    return list(reversed(data))[:limit]


async def close_report(report_id: str) -> Optional[Dict]:
    for r in _reports:
        if r["_id"] == report_id:
            r["status"]    = "resolved"
            r["closed_at"] = datetime.now(timezone.utc).isoformat()
            return r
    return None


async def get_stats() -> dict:
    cats = Counter(r["category"] for r in _reports)
    return {
        "street_damage": cats.get("street_damage", 0),
        "water_leakage": cats.get("water_leakage", 0),
        "waste_management": cats.get("waste_management", 0),
        "other_infra": cats.get("other_infra", 0),
        "total": len(_reports),
    }


# ── Users ─────────────────────────────────────────────────────────────────────

async def get_user(username: str) -> Optional[Dict]:
    return _users.get(username.lower())


async def create_user(username: str, password_hash: str) -> None:
    _users[username.lower()] = {"username": username, "password_hash": password_hash}


# ── Leaderboard ───────────────────────────────────────────────────────────────

async def get_leaderboard(limit: int = 10) -> List[Dict]:
    counts = Counter(
        r.get("username", "anonymous")
        for r in _reports
        if r.get("username")
    )
    return [{"username": u, "count": c} for u, c in counts.most_common(limit)]
