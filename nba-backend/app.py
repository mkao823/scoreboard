from fastapi import FastAPI, HTTPException
import aiohttp
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.teams import Base, Team
import asyncio
import logging
import uvicorn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
engine = create_async_engine('sqlite+aiosqlite:///nba_teams.db', echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def fetch_teams():
    url = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams'
    async with aiohttp.ClientSession() as session:
        logger.info(f"Fetching teams from {url}")
        async with session.get(url, timeout=5) as resp:
            if resp.status == 200: # success
                data = await resp.json()
                teams = data['sports'][0]['leagues'][0]['teams']
                async with async_session() as db:
                    for item in teams:
                        team = item['team']
                        team_data = {
                            'id': int(team['id']),
                            'abbreviation': team['abbreviation'],
                            'city': team['location'],
                            #'conference': team.get('conference', {}).get('name', 'N/A'),
                            #'division': team.get('division', {}).get('name', 'N/A'),
                            'full_name': team['displayName'],
                            'name': team['name']
                        }
                        db_team = Team(**team_data)
                        await db.merge(db_team)
                    await db.commit()
                logger.info("Teams fetched and stored")
                return True
            logger.error(f"Fetch failed: {resp.status}")
    return False

@app.get("/teams")
async def get_teams():
    try:
        async with async_session() as db:
            result = await db.execute('SELECT id, abbreviation, city, conference, division, full_name, name FROM teams')
            teams = result.fetchall()
            if not teams and await fetch_teams():
                result = await db.execute('SELECT id, abbreviation, city, conference, division, full_name, name FROM teams')
                teams = result.fetchall()
            logger.info(f"Returning {len(teams)} teams")
            return [{
                'id': t[0], 
                'abbreviation': t[1], 
                'city': t[2], 
                'conference': t[3],
                'division': t[4], 
                'full_name': t[5], 
                'name': t[6]
            } for t in teams]
    except Exception as e:
        logger.error(f"Error in get_teams: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/refresh")
async def refresh():
    if await fetch_teams():
        return {"status": "Teams refreshed"}
    return {"status": "Refresh failed"}, 500

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop old table
        await conn.run_sync(Base.metadata.create_all)  # Recreate
    await fetch_teams()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    asyncio.run(fetch_teams())