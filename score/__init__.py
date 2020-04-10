from .event import Event
from .time import Time
from .meet import Meet


def combine_meets(meet1, team1, meet2, team2):
    """ Combine two teams times from different meets into a single meet object.
	team1 and team2 are the teams from each meet to take
	They should be strings, either 'home' or 'away'
	The first meet listed will become the home team
	The second meet will become the away team
	Returns a meet object"""
    final_meet = Meet()

    # Ensure both meets have the same number of events
    assert len(meet1.events) == len(meet2.events)

    count = -1
    for event_to_add in meet1.events:
        count += 1
        e = event_to_add
        e2 = meet2.events[count]

        # Erase the unnecessary times
        # (prob not needed, just to be safe)
        if team1 == "home":
            e.away_times = []
        else:
            e.home_times = e.away_times[:]
            e.away_times = []

        # Add the event_to_add, without the unneeded times
        final_meet.events.append(e)

        # Erase unneeded times
        if team2 == "home":
            e2.away_times = e2.home_times[:]
            e2.home_times = []
        else:
            e2.home_times = []

        # Copy away times from the event_to_add from meet2 into the newly append event_to_add in the final_meet
        final_meet.events[-1].away_times = e2.away_times[:]

    return final_meet
