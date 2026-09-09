import os
from dotenv import load_dotenv
load_dotenv('.env')
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check():
    url = os.environ.get('DATABASE_URL')
    if not url:
        url = f"mysql+aiomysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASSWORD')}@{os.environ.get('MYSQL_HOST')}:{os.environ.get('MYSQL_PORT')}/{os.environ.get('MYSQL_DB')}"
    
    password = os.environ.get('MYSQL_PASSWORD')
    if password:
        print(url.replace(password, '***'))
        
    engine = create_async_engine(url)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text('SHOW TABLES;'))
            print('Tables:', [row[0] for row in result.fetchall()])
    except Exception as e:
        print('DB Error:', e)

asyncio.run(check())
