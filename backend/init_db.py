import os
import pymysql
from dotenv import load_dotenv

load_dotenv('.env')

pwd = os.environ.get('MYSQL_PASSWORD', 'root')
user = os.environ.get('MYSQL_USER', 'root')
host = os.environ.get('MYSQL_HOST', 'localhost')
db_name = os.environ.get('MYSQL_DB', 'railway')

try:
    print('Connecting to MySQL server...')
    conn = pymysql.connect(host=host, user=user, password=pwd)
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
        print(f'Database {db_name} ensured.')
    conn.commit()
    conn.close()
    
    print('Connecting to database and running schema...')
    conn = pymysql.connect(host=host, user=user, password=pwd, database=db_name)
    
    with open('../database/schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
        
    statements = sql.split(';')
    with conn.cursor() as cursor:
        for stmt in statements:
            if stmt.strip():
                try:
                    cursor.execute(stmt)
                except Exception as ex:
                    print('Error executing statement:', str(ex)[:100])
    conn.commit()
    print('Schema initialized.')
    conn.close()
except Exception as e:
    print('Failed:', e)
