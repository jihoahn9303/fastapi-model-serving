import os
import json

from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker
)
from sqlalchemy.exc import SQLAlchemyError


async def get_db(db_url: str):
    engine = create_async_engine(url=db_url)
    async_session = async_sessionmaker(bind=engine)
    
    async with async_session() as async_db:
        try:
            yield async_db
        except SQLAlchemyError as e:
            await async_db.rollback()
        finally:
            await async_db.close()