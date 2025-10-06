from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Dict, Any

from .db import get_session, engine, Base
from .models import Recipe

app = FastAPI()

# Allow frontend dev server to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # create tables if they don't exist (async)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def _serialize_recipe(obj: Recipe) -> Dict[str, Any]:
    """Serialize a SQLAlchemy Recipe instance to JSON-serializable dict."""
    cols = []
    if hasattr(Recipe, "__table__"):
        cols = [c.key for c in Recipe.__table__.columns]
    else:
        # Fallback - try common attribute names
        cols = ["id", "title", "ingredients", "instructions", "created_at"]

    out: Dict[str, Any] = {}
    for key in cols:
        val = getattr(obj, key, None)
        if isinstance(val, datetime):
            out[key] = val.isoformat()
        else:
            out[key] = val
    return out


@app.get("/recipes", response_model=List[Dict[str, Any]])
async def get_recipes(filter_type: str = "new", session: AsyncSession = Depends(get_session)):
    """Return recipes. Uses the async SQLAlchemy session.

    Filter types: new (default), healthiest, popular
    """
    # base query
    query = select(Recipe)

    # apply simple ordering based on filter_type if attributes exist on the model
    try:
        if filter_type == "healthiest" and hasattr(Recipe, "health_score"):
            query = query.order_by(Recipe.health_score.desc())
        elif filter_type == "popular" and hasattr(Recipe, "views"):
            query = query.order_by(Recipe.views.desc())
        else:
            # default: newest first if created_at exists
            if hasattr(Recipe, "created_at"):
                query = query.order_by(Recipe.created_at.desc())
    except Exception:
        # fallback to no ordering if model attributes differ
        pass

    result = await session.execute(query)
    rows = result.scalars().all()

    return [_serialize_recipe(r) for r in rows]