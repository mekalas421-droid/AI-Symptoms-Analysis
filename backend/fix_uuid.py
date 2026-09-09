import os, pymysql
from dotenv import load_dotenv

load_dotenv('.env')

conn = pymysql.connect(
    host=os.environ.get('MYSQL_HOST', 'localhost'),
    user=os.environ.get('MYSQL_USER', 'root'),
    password=os.environ.get('MYSQL_PASSWORD', 'root'),
    database=os.environ.get('MYSQL_DB', 'railway')
)
with conn.cursor() as cur:
    cur.execute("UPDATE symptoms_master SET id = REPLACE(id, '-', '')")
conn.commit()
conn.close()
print('Dashes removed')
