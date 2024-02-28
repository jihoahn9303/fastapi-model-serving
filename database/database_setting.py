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
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_port = os.getenv("MYSQL_PORT")
    mysql_database_name = os.getenv("MYSQL_DATABASE_NAME")
    
    database_urls = [
        "mysql+aiomysql://", 
        mysql_user, ":", 
        mysql_password, "@",
        mysql_host, ":",
        mysql_port, "/",
        mysql_database_name
    ]
    
    return "".join(database_urls)


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