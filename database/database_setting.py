import os
import json

from dotenv import load_dotenv
print('find dot env: ', load_dotenv())

from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker
)
from sqlalchemy.exc import SQLAlchemyError


def get_database_url() -> str:
    mysql_user = os.getenv("MYSQL_USER")[1:]
    mysql_password = os.getenv("MYSQL_PASSWORD")[1:]
    mysql_host = os.getenv("MYSQL_HOST")[1:]
    mysql_port = os.getenv("MYSQL_PORT")[1:]
    mysql_database_name = os.getenv("MYSQL_DATABASE_NAME")[1:]
    
    return f"mysql+aiomysql://${mysql_user}:${mysql_password}@${mysql_host}:${mysql_port}/${mysql_database_name}"


async def get_db():
    database_url = get_database_url()
    print('database_url: ', database_url)
    engine = create_async_engine(url=database_url)
    async_session = async_sessionmaker(bind=engine)
    
    async with async_session() as async_db:
        try:
            yield async_db
        except SQLAlchemyError as e:
            await async_db.rollback()
        finally:
            await async_db.close()