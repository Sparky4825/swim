from bs4 import BeautifulSoup
import requests
from .swimmer import Swimmer
from datetime import datetime


def fetch_meet_results(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, features="html.parser")
    table = soup.select('body > form:nth-child(1) > table:nth-child(15)')[0]

    results = []
    for row in table.find_all('tr')[1:-1]:
        results.append([])
        for cell in row.find_all('td'):
            results[-1].append(cell.text)

    events = []
    # Format: [EVENT NAME,
    # [[HOME TIME, SWIMMER NAME], [HOME TIME, SWIMEER NAME]],
    # [[AWAY TIME, SWIMMER NAME], [AWAY TIME, SWIMMER NAME]]]

    # Options are:
    # event
    # times
    # exhib
    current_parse = 'event'

    for row in results:
        print(row)
        if 'Exhibition' in row[0]:
            print('starting exhibition')
            current_parse = 'exhib'

        # Start new event if only a single element in row
        elif len(row) == 1:
            events.append([row[0], [], []])
            current_parse = 'times'

        # If at new event, add list to the list of events and add event name
        elif current_parse == 'event':
            events.append([row[0], [], []])
            current_parse = 'times'

        # If parsing times, add a new time to the last event
        elif current_parse == 'times':
            if row[0] == '' and row[7] == '':
                # if on to the next event
                current_parse = 'event'
            else:
                # Add home times to the event
                events[-1][1].append([row[1], row[0]])

                # Add away times to the event
                events[-1][2].append([row[7], row[6]])

        elif current_parse == 'exhib':
            # Scan until the end of the exhibition, then start the next event
            if len(row) == 1:
                print('done with exhibnition')
                current_parse = 'times'
                events.append([row[0], [], []])

    return events


def time_to_float(time):
    try:
        return float(time)
    except ValueError:
        if time is None or 'dq' in time.lower():
            return None
        return int(time.split(':')[0]) * 60 + float(time.split(':')[1])


def fetch_swimmer(url):
    '''Downloads the information and times for a swimmer at the given url'''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")

    # Years of graduation to year name
    graduation = {
        2020: 'SR',
        2021: 'JR',
        2022: 'SO',
        2023: 'FR',
        2024: '\'8',
        2025: '\'7'
    }

    info = soup.select('table')[0]

    # Extract the name of the swimmer
    last = info.select('td')[1].select('b')[0].text
    first = info.select('td')[2].select('b')[0].text

    year = info.select('td')[9].select('b')[0].text
    year = graduation[int(year)]

    name = first + ' ' + last
    swim = Swimmer(name, year)

    try:
        times = soup.select('table')[2].select('tr')
        current_event = times[0].text

        for i in times:
            if '<b>' in str(i):
                current_event = i.text
            else:
                swim.times.append(
                    Swimmer.Time(current_event,
                                 datetime.strptime(i.text[:10], '%m/%d/%Y'),
                                 time_to_float(i.text[13:])))

    except IndexError:
        times = []

    return swim


def fetch_team_urls():
    '''Fetch all the urls for all of the teams in section III'''

    # Gets all of the teams
    url = 'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/WebTeams\
?OpenView'

    # Parse the pages
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features='html.parser')

    # Extract team names and urls
    dropdown = soup.find_all('option')

    # Format: [name, url]
    teams = []
    # Skip the first option because it is the menu title
    for i in dropdown[1:]:
        teams.append([i.text, i['value']])

    return teams


def fetch_swimmer_urls(url):
    '''Fetch all of the swimmers and urls from a team url'''

    # Download/parse the pages
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features='html.parser')

    # The last table in the page contains all the swimmers
    table = soup.find_all('table')[-1]

    # Each swimmer is a link in the table
    links = table.find_all('a')

    # Format: [name and year, url]
    swimmers = []
    for i in links:
        if i is not None:
            swimmers.append([i.text, 'http://www.swimdata.info' + i['href']])

    return swimmers


def fetch_meet_urls(url):
    '''Fetch all of the urls for the meets that the team has been in
    return [[text, date, url]]'''

    # Download the page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features='html.parser')

    # Select the table with the meet urls
    table = soup.find_all('table')[-3]

    meets = []
    for i in table.find_all('tr'):
        t = i.find_all('td')
        if len(i.find_all('a')) > 0:
            meets.append([str(t[1].text), str(t[0].text), i.find_all('a')[0]['href']])

    return meets
