import pandas as pd
import sqlite3

urls = pd.read_csv("urls.csv")

class find:
    def team_date(team, date):
        for index, row in urls.iterrows():
            if row[0] == date and (team.lower() == row[1].lower() or team.lower() == row[2].lower()):
                return row[3]

conn = sqlite3.connect('swim.db')

def add_swimmer(name, year, team):

    sql = '''INSERT INTO swimmers (name, year, team)
    VALUES (?, ?, ?) '''

    cur = conn.cursor()
    cur.execute(sql, [name, year, team])

def add_race(name, team, event, time, timestr,date):
    sql = '''INSERT INTO times (name, team, event, time, time_readable, date)
    VALUES (?, ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, [name, team, event, time, timestr, date])

def close_connection():
    conn.commit()
    conn.close()


def clear_database():
    allow = input('Program is requesting to EMPTY the database. Allow? y/[N] ')
    if allow.lower() == 'y':
        sql = 'DELETE FROM swimmers'
        cur = conn.cursor()
        cur.execute(sql)

        sql = 'DELETE FROM times'
        cur.execute(sql)
