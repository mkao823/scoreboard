# daily schedule 
import aiohttp
import logging

from fastapi import HTTPException
from databases.db import async_session
from models.teams import Team
from app import app

async def fetch_events():
    # returns games for the day, contains some live data such as time remaining for each game if started, as well as general info such as home team, away team, start time, etc
    url = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/events'


    
#async def get_events():