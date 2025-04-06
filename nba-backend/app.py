from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from databases.db import engine, async_session
from services.teams import fetch_teams, get_teams
from services.events import get_events
from models.teams import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await fetch_teams() 

app = FastAPI(lifespan=lifespan)

@app.get("/teams")
async def teams_endpoint():
    return await get_teams()

@app.get("/events")
async def events_endpoint():
    return await get_events()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)