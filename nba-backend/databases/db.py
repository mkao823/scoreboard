from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# SQLite for static data
engine = create_async_engine('sqlite+aiosqlite:///nba_teams.db', echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
