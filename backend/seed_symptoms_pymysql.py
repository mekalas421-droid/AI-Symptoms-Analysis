import os
import pymysql
import json
import uuid
from dotenv import load_dotenv

load_dotenv('.env')

from app.db.seed import SYMPTOMS_DATA, normalize_code

pwd = os.environ.get('MYSQL_PASSWORD', 'root')
user = os.environ.get('MYSQL_USER', 'root')
host = os.environ.get('MYSQL_HOST', 'localhost')
db_name = os.environ.get('MYSQL_DB', 'railway')

try:
    conn = pymysql.connect(host=host, user=user, password=pwd, database=db_name)
    with conn.cursor() as cursor:
        for category, symptoms in SYMPTOMS_DATA.items():
            for s_name in symptoms:
                s_code = normalize_code(s_name)
                syns = json.dumps([s_name.lower()])
                uid = str(uuid.uuid4())
                try:
                    cursor.execute(
                        "INSERT IGNORE INTO symptoms_master (id, symptom_code, display_name, category, synonyms) VALUES (%s, %s, %s, %s, %s)",
                        (uid, s_code, s_name, category, syns)
                    )
                except Exception as e:
                    pass
    conn.commit()
    conn.close()
    print('Successfully seeded symptoms using pymysql.')
except Exception as e:
    print('Failed:', e)
