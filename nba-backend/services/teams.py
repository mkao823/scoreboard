import aiohttp
import logging

from fastapi import HTTPException
from databases.db import async_session
from models.teams import Team
from app import app

logger = logging.getLogger(__name__)

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

async def get_team_ids():
    try:
        async with async_session() as db:
            result = await db.execute('SELECT id FROM teams')
            team_ids = [row[0]for row in result.fetchall()]
            if not team_ids and await fetch_teams():
                result = await db.execute('SELECT id FROM teams')
                team_ids = [row[0] for row in result.fetchall()]
            logger.info(f"Returning {len(team_ids)} team IDs")
            return team_ids
    except Exception as e:
        logger.error(f"Error in get_team_ids: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def fetch_rosters():
    team_ids = await get_team_ids()
    rosters = []
    

async def fetch_team_stats():
    # static data, can be refreshed at least once a day, or once the teams game ends
    # different total stats for teams such as shot percentage, total 2 pointers, total blocks, etc. may be able to specify year in the call to get past data
    id = 2 # one team for now but need to loop through all team ids, (1-30 ?) and fetch stats
    url = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{id}/statistics' # 2 denotes id for team, need to 


