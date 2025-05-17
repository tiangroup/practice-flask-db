from flask import Flask
from markupsafe import escape
import os
import pymysql.cursors

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


@app.route("/")
def index():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM goods")
                rows = cur.fetchall()

        if rows:
            items = "\n".join(f"<li>{escape(r['name'])}</li>" for r in rows)
            html = f"<ul>\n{items}\n</ul>"
        else:
            html = "<p>Нет данных</p>"

    except Exception as exc:
        html = f"<p>Ошибка подключения: {escape(str(exc))}</p>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
