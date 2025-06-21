from decouple import config
import psycopg2

try:
    url = config("DATABASE_URL")
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    print("Connected! Time:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("Failed:", e)
