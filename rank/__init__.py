import data
import numpy as np
from scipy import stats


def rank_swim(time, event, date=None):
    """Creates a percentile ranking for a time given the event, date and time.
    Returns a float where higher is a faster time"""

    if time is None:
        return 0

    if date is not None:
        all_swims = data.search_races(event=event, date=date)
    else:
        all_swims = data.search_races(event=event)

    all_times = []
    for i in all_swims:
        if i[5] is not None:
            all_times.append(float(i[5]))

    return round(100 - stats.percentileofscore(all_times, time), 2)


def get_weight(x):
    """Calculate the weight for a swimmer based on their place in the team"""
    return max([10 - (1 * 1.6 ** x), 0])


def rank_swimmer(name, team=None, count_diving=False):
    """Averages all the scores for all of the swimmer's races"""
    all_swims = data.search_races(name=name, team=team)

    percentiles = []
    for race in all_swims:
        if 'diving' in race[3].lower() and not count_diving:
            continue
        percentiles.append(rank_swim(race[5], race[3], race[6]))

    if len(percentiles) == 0:
        return None

    return round(float(np.mean(percentiles)), 2)


def rank_team(team_name, display_swimmers=False):
    """Averages all of the swimmers scores on the team"""

    # weights = [
    #     1,
    #     1,
    #     1,
    #     0.9,
    #     0.6,
    #     0.3,
    #     0.1,
    # ]

    swimmers = data.search_swimmer(team=team_name)
    swimmers_name = []
    for i in swimmers:
        swimmers_name.append(i[1])

    ranks = []
    for i in swimmers_name:
        swim_rank = rank_swimmer(i, team_name)
        if swim_rank is not None and not np.isnan(swim_rank):
            ranks.append(swim_rank)
            if display_swimmers:
                print(i, swim_rank)

    # Teams must have at least 12 people, add zeros to make 12 people
    # TODO: min team size for ranking is arbitrary, determine better value
    while len(ranks) < 12:
        ranks.append(0)

    ranks.sort(reverse=True)
    count = -1
    ranks_values = []
    ranks_weights = []
    for i in ranks:
        count += 1
        # if count >= len(weights):
        #     break

        ranks_values.append(i)
        ranks_weights.append(get_weight(count))
    # print(ranks_weights)
    return round(np.average(ranks_values, weights=ranks_weights), 2)
