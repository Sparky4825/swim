import data
import fetch


# swimmers = fetch.fetch_swimmer_urls('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Teams%20List/Cooperstown
# ?OpenDocument')


def download_everything():
    # Clear out old data
    data.clear_database()

    # Download list of all teams
    teams = fetch.fetch_team_urls()

    for t in teams:
        # Download all swimmers
        team = t[0]
        print('Downloading {}... '.format(team), end='')

        download_team_from_url(t[1])
        print('done')


def download_team_from_url(url, team):
    swimmers = fetch.fetch_swimmer_urls(url)

    for i in swimmers:
        # Download the swimmers
        swim = fetch.fetch_swimmer(i[1])

        # Add to the list of swimmers
        data.add_swimmer(swim.name, swim.year, team)

        # Add all of the times
        for time in swim.times:
            data.add_race(swim.name, team, time.name, time.time, time.date)


def download_teams(name):
    # Download list of all teams
    teams = fetch.fetch_team_urls()

    names_lower = []
    for i in name:
        names_lower.append(i.lower())

    for t in teams:
        if t[0].lower() in names_lower:
            download_team_from_url(t[1], t[0])


data.clear_database()

download_teams(['Cooperstown', 'Proctor'])

data.close_connection()
