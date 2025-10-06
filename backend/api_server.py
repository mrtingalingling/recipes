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
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=[*],
    allow_headers=[*],
)


@app.on_event(startup)
async def startup():
    # create tables if they don't exist (async)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get(/recipes)
async def get_recipes(filter_type: str = new, session: AsyncSession = Depends(get_session)):
    Return
