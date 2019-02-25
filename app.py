import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all local GET requests
    sql_all_local = """SELECT COUNT(*) FROM weblogs WHERE source LIKE \'local\';"""
    cur.execute(sql_all_local)
    all_local = cur.fetchone()[0]

    # Get number of all successful local requests
    sql_success_local = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' AND source LIKE \'local\';"""
    cur.execute(sql_success_local)
    success_local = cur.fetchone()[0]

    # Determine rate if there was at least one request
    rateLocal = "No entries yet!"
    if all_local != 0:
        rateLocal = str(success_local / all_local)

    # Get number of all remote GET requests
    sql_all_remote = """SELECT COUNT(*) FROM weblogs WHERE source LIKE \'remote\';"""
    cur.execute(sql_all_remote)
    all_remote = cur.fetchone()[0]

    # Get number of all successful remote requests
    sql_success_remote = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' AND source LIKE \'remote\';"""
    cur.execute(sql_success_remote)
    success_remote = cur.fetchone()[0]

    # Determine rate if there was at least one request
    rateRemote = "No entries yet!"
    if all_remote != 0:
        rateRemote = str(success_remote / all_remote)

    return render_template('index.html', rateLocal = rateLocal, rateRemote = rateRemote)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
