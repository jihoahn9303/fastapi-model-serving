import os
import json

from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker
)
from sqlalchemy.exc import SQLAlchemyError


async def get_db():
    MYSQL_DATABASE_URL = json.loads(os.getenv("MYSQL_DATABASE_URL"))["url"]

    engine = create_async_engine(url=MYSQL_DATABASE_URL)
    async_session = async_sessionmaker(bind=engine)
    
    async with async_session() as async_db:
        try:
            yield async_db
        except SQLAlchemyError as e:
            await async_db.rollback()
        finally:
            await async_db.close()