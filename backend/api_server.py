from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    # create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/recipes")
async def get_recipes(filter_type: str = "new", session: AsyncSession = Depends(get_session)):
    query = select(Recipe).order_by(Recipe.created_at.desc())
    if filter_type == "healthiest":
        query = select(Recipe).where(Recipe.instructions.ilike('%healthy%')).order_by(Recipe.created_at.desc())
    elif filter_type == "popular":
        query = select(Recipe).order_by(Recipe.id.desc()).limit(10)
    result = await session.execute(query)
    rows = result.scalars().all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "ingredients": r.ingredients,
            "instructions": r.instructions,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
