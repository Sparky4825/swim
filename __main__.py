import fetch
import score

# HP
results = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent%20vs%20Cooperstown%20on%2012-3-2019?OpenDocument')
# results2 = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent%20vs%20Cooperstown%20on%2012-3-2019?OpenDocument')
#RFA
results2 = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Rome%20Free%20Academy%20vs%20Cooperstown%20on%2012-5-2019?OpenDocument')

meet = score.Meet()
meet2 = score.Meet()

final = score.Meet()

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
            # print(home_times[-1].name)

    for t in e[2]:
        if t[1] != '':
            away_times.append(score.Time(t[1], time_to_float(t[0])))
            # print(away_times[-1].name)


    # Add the events
    event = score.Event(e[0], home_times, away_times, 'relay' in e[0].lower(), 'diving' in e[0].lower())
    meet.events.append(event)
print('-' * 10)
for e in results2:
    home_times = []
    away_times = []

    # Add time objects with times from the list for home and away teams
    for t in e[1]:
        if t[1] != '':
            home_times.append(score.Time(t[1], time_to_float(t[0])))
            # print(home_times[-1].name)
    for t in e[2]:
        if t[1] != '':
            away_times.append(score.Time(t[1], time_to_float(t[0])))
            # print(away_times[-1].name)


    # Add the events
    event = score.Event(e[0], home_times, away_times, 'relay' in e[0].lower(), 'diving' in e[0].lower())
    meet2.events.append(event)

# TEST ONLY
# Take times from home teams in both meets and score
count = -1
for event in meet.events:

    count += 1
    # print(event.name)
    meet2.events[count].home_times = event.away_times
    for i in event.away_times:
        print(i.name)

for event in meet2.events:
    for t in event.home_times:
        print(t.name, t)

# print(meet2.score(True))
