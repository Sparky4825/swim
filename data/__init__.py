import sqlite3


conn = sqlite3.connect('swim.db')


def add_swimmer(name, year, team):
    sql = '''INSERT INTO swimmers (name, year, team)
    VALUES (?, ?, ?) '''

    cur = conn.cursor()
    cur.execute(sql, [name, year, team])


def add_race(name, team, event, time, time_str, date, relay_split=False, exhib=False):
    sql = '''INSERT INTO times (name, team, event, time, time_readable, date, relay_split, exhibition)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, [name, team, event, time, time_str, date, int(relay_split), int(exhib)])


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
    (id, name, year, team)
    or None if no swimmer is found

    Returns list if more than one found"""

    # Return none if no conditions set
    if name is None and team is None and year is None:
        return None

    if name is not None:
        name = name.lower()

    if team is not None:
        team = team.lower()

    if year is not None:
        year = year.lower()

    # Get cursor
    cur = conn.cursor()

    # Set sql query
    sql = '''SELECT * FROM swimmers WHERE '''
    conditions = []
    conditions_parameters = []

    if name is not None:
        conditions.append("lower(name) LIKE ?")
        conditions_parameters.append('%{}%'.format(name))

    if team is not None:
        conditions.append("lower(team) LIKE ?")
        conditions_parameters.append('%{}%'.format(team))

    if year is not None:
        conditions.append("lower(year) LIKE ?")
        conditions_parameters.append('%{}%'.format(year))

    sql += ' AND '.join(conditions)

    cur.execute(sql, conditions_parameters)
    rows = cur.fetchall()

    if len(rows) == 1:
        return rows[0]
    else:
        return rows


def search_races(name=None, event=None, date=None, team=None, relay_split=None):
    """Search the database for races that match the given criteria
    Returns a list of matching races, even if there is only one race

    Note: event name must match exactly (case insensitive) because of relays"""

    # None if nothing given
    if name is None and event is None and date is None and team is None and relay_split is None:
        return None

    # Get cursor
    cur = conn.cursor()

    # Set sql query
    sql = '''SELECT * FROM times WHERE '''
    conditions = []
    conditions_parameters = []

    # Set all parameters to lowercase and search
    if name is not None:
        name = name.lower()
        conditions.append('lower(name) LIKE ?')
        conditions_parameters.append('%{}%'.format(name))

    if event is not None:
        event = event.lower()
        conditions.append('lower(event) LIKE ?')
        if 'diving' not in event:
            conditions_parameters.append(event)
        else:
            conditions_parameters.append('%{}%'.format(event))

    if date is not None:
        date = date.lower()
        conditions.append('lower(date) LIKE ?')
        conditions_parameters.append('%{}%'.format(date))

    if team is not None:
        team = team.lower()
        conditions.append('lower(team) LIKE ?')
        conditions_parameters.append('%{}%'.format(team))

    if relay_split is not None:
        if relay_split:
            conditions.append('relay_split = 1')
        else:
            conditions.append('relay_split = 0')

    sql += ' AND '.join(conditions)

    cur.execute(sql, conditions_parameters)
    return cur.fetchall()

