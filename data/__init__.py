import pandas as pd
import sqlite3

urls = pd.read_csv("urls.csv")


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


def add_race(name, team, event, time, time_str, date):
    sql = '''INSERT INTO times (name, team, event, time, time_readable, date)
    VALUES (?, ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, [name, team, event, time, time_str, date])


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


def search_swimmer(name=None, team=None, year=None):
    """Searches the database for a swimmer and returns their information in the format:
    [name, team, year]
    or None if no swimmer is found"""

    # Return none if no conditions set
    if name is None and team is None and year is None:
        return None

    # Get cursor
    cur = conn.cursor()

    # Set sql query
    sql = '''SELECT * FROM swimmers WHERE '''
    conditions = []
    conditions_parameters = []

    if name is not None:
        conditions.append("name LIKE ?")
        conditions_parameters.append('%{}%'.format(name))

    if team is not None:
        conditions.append("team LIKE ?")
        conditions_parameters.append('%{}%'.format(team))

    if year is not None:
        conditions.append("year LIKE ?")
        conditions_parameters.append('%{}%'.format(year))

    sql += ' AND '.join(conditions)

    cur.execute(sql, conditions_parameters)
    rows = cur.fetchall()

    for row in rows:
        print(row)
