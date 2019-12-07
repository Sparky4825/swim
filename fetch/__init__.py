from bs4 import BeautifulSoup
import requests
from .swimmer import Swimmer
from datetime import datetime

def fetch_meet_results(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, features="html.parser")
    table = soup.select('body > form:nth-child(1) > table:nth-child(15)')[0]

    results = []
    for row in table.find_all('tr')[1:-2]:
        results.append([])
        for cell in row.find_all('td'):
            results[-1].append(cell.text)

    events = []
    # Format: [EVENT NAME, [[HOME TIME, SWIMMER NAME], [HOME TIME, SWIMEER NAME]], [[AWAY TIME, SWIMMER NAME], [AWAY TIME, SWIMMER NAME]]]

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

        # If at a new event, add a new list to the list of events and add the event name
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
    except:
        if time is None or 'dq' in time.lower():
            return None
        return int(time.split(':')[0]) * 60 + float(time.split(':')[1])

def fetch_swimmer(url):
    '''Downloads the information and times for a swimmer at the given url'''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")

    # Extract the name of the swimmer
    last = soup.select('table')[0].select('td')[1].select('b')[0].text
    first = soup.select('table')[0].select('td')[2].select('b')[0].text

    name = first + ' ' + last
    swim = Swimmer(name)

    times = soup.select('table')[2].select('tr')

    current_event = times[0].text
    for i in times:
        if '<b>' in str(i):
            current_event = i.text
        else:
            swim.times.append(Swimmer.Time(current_event, datetime.strptime(i.text[:10], '%m/%d/%Y'), time_to_float(i.text[13:])))
    return swim

# for i in fetch_swimmer('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Teams/3118F78CA16E4E49862581DD000ABC4A?OpenDocument').times:
for i in fetch_swimmer('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Teams/DAA9D0E8252AD0A586258080006E3E44?OpenDocument').times:
    print(i.name, i.date, i.time)
