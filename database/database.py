import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker
)
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()


MYSQL_DATABASE_URL = os.environ["MYSQL_DATABASE_URL"]

engine = create_async_engine(url=MYSQL_DATABASE_URL)
async_session = async_sessionmaker(bind=engine)


async def get_db():
    async with async_session() as async_db:
        try:
            yield async_db
        except SQLAlchemyError as e:
            await async_db.rollback()
        finally:
            await async_db.close()