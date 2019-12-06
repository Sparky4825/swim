import fetch
import score

# HP
results = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent%20vs%20Cooperstown%20on%2012-3-2019?OpenDocument')
#RFA
results = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Rome%20Free%20Academy%20vs%20Cooperstown%20on%2012-5-2019?OpenDocument')

meet = score.Meet()

def time_to_float(time):
    try:
        return float(time)
    except:
        if time is None or 'dq' in time.lower():
            return None
        return int(time.split(':')[0]) * 60 + float(time.split(':')[1])

for e in results:
    home_times = []
    away_times = []

    # Add time objects with times from the list for home and away teams
    for t in e[1]:
        if t[1] != '':
            home_times.append(score.Time(t[1], time_to_float(t[0])))
    for t in e[2]:
        if t[1] != '':
            away_times.append(score.Time(t[1], time_to_float(t[0])))

    # Add the events
    event = score.Event(e[0], home_times, away_times, 'relay' in e[0].lower(), 'diving' in e[0].lower())
    meet.events.append(event)

print(meet.score(True))
