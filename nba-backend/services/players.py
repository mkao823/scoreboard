#
import aiohttp
import logging

from fastapi import HTTPException
from databases.db import async_session
from models.teams import Team
from app import app

async def get_rosters():
    id = 1
    url = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{id}/roster'
    '''
    ex:
    "id": "3917376",
            "uid": "s:40~l:46~a:3917376",
            "guid": "0d5cde01-f6d3-225f-dae5-44ef3304cda2",
            "alternateIds": {
                "sdr": "3917376"
            },
            "firstName": "Jaylen",
            "lastName": "Brown",
            "fullName": "Jaylen Brown",
            "displayName": "Jaylen Brown",
            "shortName": "J. Brown",
            "weight": 223.0,
            "displayWeight": "223 lbs",
            "height": 78.0,
            "displayHeight": "6' 6\"",
            "age": 28,
            "dateOfBirth": "1996-10-24T07:00Z",
            "debutYear": 2016,
    '''