import data
import fetch
import score


# # Coop @ HP (12/03/2019)
# results = fetch.fetch_meet_results(
#     'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent%20vs%20Cooperstown%20on%2012-3'
#     '-2019?OpenDocument')
#
# # Coop @ RFA (12/05/2019)
# results2 = fetch.fetch_meet_results(
#     'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Rome%20Free%20Academy%20vs%20Cooperstown%20on'
#     '%2012-5-2019?OpenDocument')
#
# # HP @ Proctor (12/05/2019)
# results3 = fetch.fetch_meet_results(
#     'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Proctor%20vs%20Holland%20Patent%20on%2012-5-2019'
#     '?OpenDocument')
#
# # Sherburne @ HP (12/10/2019)
# results4 = fetch.fetch_meet_results(
#     'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent%20vs%20Sherburne%20Earlville'
#     '%20on%2012-10-2019?OpenDocument')
#
# # Proctor @ Coop (12/10/2019)
# results5 = fetch.fetch_meet_results(
#     'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Cooperstown%20vs%20Proctor%20on%2012-10-2019'
#     '?OpenDocument')
#
# # Oneida @ Sherburne (12/05/2019)
# results6 = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Sherburne'
#                                     '%20Earlville%20vs%20Oneida%20on%2012-5-2019?OpenDocument')
#
# # Sherburne @ RFA (12/03/2019)
# results7 = fetch.fetch_meet_results(
#     'http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Rome%20Free%20Academy%20vs%20Sherburne'
#     '%20Earlville%20on%2012-3-2019?OpenDocument')
#
# # Oneida @ HP (12/12/2019)
# results8 = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Holland%20Patent'
#                                     '%20vs%20Oneida%20on%2012-12-2019?OpenDocument')
#
# # Coop @ SE (12/12/2019)
# results9 = fetch.fetch_meet_results('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Meet%20List/Sherburne'
#                                     '%20Earlville%20vs%20Cooperstown%20on%2012-12-2019?OpenDocument')


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


def meet_from_db(team1, date1, team2, date2):
    """Creates a meet object from times in the database"""

    final_meet = score.Meet()

    all_events = [
        '200 Medley Relay',
        '200 Freestyle',
        '200 Individual Medley',
        '50 Freestyle',
        'Diving',
        '100 Butterfly',
        '100 Freestyle',
        '500 Freestyle',
        '200 Freestyle Relay',
        '100 Backstroke',
        '100 Breaststroke',
        '400 Freestyle Relay'
    ]

    for current_event in all_events:
        # Search for matching times
        team1_times_rows = data.search_races(event=current_event, date=date1, team=team1, relay_split=False)
        team2_times_rows = data.search_races(event=current_event, date=date2, team=team2, relay_split=False)

        home_times = []
        home_swimmers = []
        away_times = []
        away_swimmers = []

        is_relay = 'relay' in current_event.lower()
        is_diving = 'diving' in current_event.lower()

        # Add all matching times to the meet
        for time in team1_times_rows:
            # Only use a swimmer once (because times from relays are also added to db, and swimmers could race more
            # than once in the same event and not an exhibition swimmer
            if time[1] not in home_swimmers and time[8] == 0:
                home_times.append(score.Time(time[1], time[5]))
                home_swimmers.append(time[1])

        # Team 2
        for time in team2_times_rows:
            if time[1] not in away_swimmers and time[8] == 0:
                away_times.append(score.Time(time[1], time[5]))
                away_swimmers.append(time[1])

        final_meet.events.append(score.Event(current_event, home_times, away_times, is_relay, is_diving))

    return final_meet


# m1 = results_to_meet(results)
# m2 = results_to_meet(results2)
# m3 = results_to_meet(results3)
# m4 = results_to_meet(results4)
# m5 = results_to_meet(results5)
# m6 = results_to_meet(results6)
# m7 = results_to_meet(results7)
# m8 = results_to_meet(results8)
# m9 = results_to_meet(results9)
# m
# m1.score(True)
# m2.score(True)

# m = score.combine_meets(m8, 'away', m9, 'away')
# m.score(True, entries=2)
# data.clear_database()
# download.download_times_from_league_meets()
# download.download_all_relays()
date = '2019-12-19'
meet_from_db('Cooperstown', date, 'Sherburne Earlville', date).score(True, entries=2)

data.close_connection()
