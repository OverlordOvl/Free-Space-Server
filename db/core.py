from Core import settings

import psycopg2
conn = psycopg2.connect(dbname=settings.DB_NAME, user='db_user',
                        password='mypassword', host='localhost')
cursor = conn.cursor()