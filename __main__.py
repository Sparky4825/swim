import fetch
import score

# Coop @ HP (12/03/2019)
results = fetch.fetch_meet_results(
    'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent%20vs%20Cooperstown%20on%2012-3'
    '-2019?OpenDocument')

# Coop @ RFA (12/05/2019)
results2 = fetch.fetch_meet_results(
    'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Rome%20Free%20Academy%20vs%20Cooperstown%20on'
    '%2012-5-2019?OpenDocument')

# HP @ Proctor (12/05/2019)
results3 = fetch.fetch_meet_results(
    'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Proctor%20vs%20Holland%20Patent%20on%2012-5-2019'
    '?OpenDocument')

# Sherburne @ HP (12/10/2019)
results4 = fetch.fetch_meet_results(
    'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent%20vs%20Sherburne%20Earlville'
    '%20on%2012-10-2019?OpenDocument')

# Proctor @ Coop (12/10/2019)
results5 = fetch.fetch_meet_results(
    'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Cooperstown%20vs%20Proctor%20on%2012-10-2019'
    '?OpenDocument')

# Oneida @ Sherburne (12/05/2019)
results6 = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Sherburne'
                                    '%20Earlville%20vs%20Oneida%20on%2012-5-2019?OpenDocument')

# Sherburne @ RFA (12/03/2019)
results7 = fetch.fetch_meet_results(
    'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Rome%20Free%20Academy%20vs%20Sherburne'
    '%20Earlville%20on%2012-3-2019?OpenDocument')


def results_to_meet(results_array):
    """Takes results_array from fetch.fetch_meet_results() and converts
    it to a meet object"""

    meet = score.Meet([])

    for e in results_array:
        home_times = []
        away_times = []

        # Add time objects with times from the list for home and away teams
        for t in e[1]:
            if t[1] != '':
                home_times.append(score.Time(t[1], fetch.time_to_float(t[0])))
        for t in e[2]:
            if t[1] != '':
                away_times.append(score.Time(t[1], fetch.time_to_float(t[0])))

        # Add the events
        event = score.Event(e[0], home_times, away_times, 'relay' in e[0].lower(), 'diving' in e[0].lower())
        meet.events.append(event)

    return meet


m1 = results_to_meet(results)
m2 = results_to_meet(results2)
m3 = results_to_meet(results3)
m4 = results_to_meet(results4)
m5 = results_to_meet(results5)
m6 = results_to_meet(results6)
m7 = results_to_meet(results7)
# m
# m1.score(True)
# m2.score(True)

m = score.combine_meets(m5, 'home', m4, 'away')
m.score(True, entries=2)
