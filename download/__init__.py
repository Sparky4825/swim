import data
import fetch


# swimmers = fetch.fetch_swimmer_urls('http://www.swimdata.info/NYState/Sec3/BSwimMeet.nsf/Teams%20List/Cooperstown
# ?OpenDocument')


def download_everything():
    """Downloads every from section III"""
    # Download list of all teams
    teams_to_download = fetch.fetch_team_urls()

    for t in teams_to_download:
        # Download all swimmers
        team = t[0]
        print("Downloading {}... ".format(team), end="")

        download_team_from_url(t[1], team)
        print("done")

    # Also download relays
    download_all_relays()


def download_team_from_url(url, team, swimmers_only=False):
    """Downloads info about a single team from url"""
    swimmers = fetch.fetch_swimmer_urls(url)

    for i in swimmers:
        # Download the swimmers
        swim = fetch.fetch_swimmer(i[1])

        # Add to the list of swimmers
        data.add_swimmer(swim.name, swim.year, team)
        if not swimmers_only:
            # Add all of the times
            for time in swim.times:
                data.add_race(
                    swim.name, team, time.name, time.time, str(time), time.date
                )

    # Download meets to get relays


def download_teams(name, swimmers_only=False):
    # Download list of all teams
    teams_to_download = fetch.fetch_team_urls()

    names_lower = []
    for i in name:
        names_lower.append(i.lower())

    for t in teams_to_download:
        if t[0].lower() in names_lower:
            print("Downloading {}... ".format(t[0]), end="")
            download_team_from_url(t[1], t[0], swimmers_only=swimmers_only)
            print("done")


def download_league_teams(swimmers_only=False):
    """Download all of the teams from our league"""
    teams = [
        "Cooperstown",
        "Proctor",
        "Holland Patent",
        "Oneida",
        "Rome Free Academy",
        "Sherburne Earlville",
    ]
    download_teams(teams, swimmers_only=swimmers_only)


def download_relays(meet_url, home_team, away_team, date):
    """Fetch all of the relays from the meet at the url and save them to the
    database"""

    meet = fetch.fetch_meet_results(meet_url)

    # Loop through all races
    for race in meet:

        # If the race is a relay, add it
        if "relay" in race[0].lower():
            # Add all the home times
            for home_race in race[1]:
                # Continue if empty race
                if home_race[0] == "":
                    continue
                data.add_race(
                    home_race[1],
                    home_team,
                    race[0],
                    fetch.time_to_float(home_race[0]),
                    home_race[0],
                    date,
                )

            # Add all the away times
            for away_race in race[2]:
                # Continue if empty race
                if away_race[0] == "":
                    continue
                data.add_race(
                    away_race[1],
                    away_team,
                    race[0],
                    fetch.time_to_float(away_race[0]),
                    away_race[0],
                    date,
                )


def download_all_relays():
    """Download all the relays from section III"""
    meet_urls = fetch.fetch_all_meet_urls()
    for i in meet_urls:
        # Extract team names from url
        names = i.split("/")[-1]
        names = names.replace("%20", " ")

        home_team = names.split(" vs ")[0]
        away_team = names.split(" vs ")[1].split(" on ")[0]

        # Extract and format date
        date = names.split(" vs ")[1].split(" on ")[1].split("?")[0]
        date = date.split("-")
        date_reformatted = "{}-{}-{}".format(
            date[2].zfill(2), date[0].zfill(2), date[1].zfill(2)
        )

        download_relays(i, home_team, away_team, date_reformatted)


def download_times_from_league_meets():
    """Download all the times from league meets"""
    meet_urls = fetch.fetch_all_meet_urls()

    teams = [
        "Cooperstown",
        "Proctor",
        "Holland Patent",
        "Oneida",
        "Rome Free Academy",
        "Sherburne Earlville",
    ]

    for meet_url in meet_urls:
        contains_league_team = False

        # Check that url contains a league team
        for i in teams:
            if i in meet_url:
                contains_league_team = True
                break

        # If not, continue and not download
        if contains_league_team is False:
            continue
        print("Downloading meet: ", meet_url)
        download_all_times_from_meet(meet_url)


def download_all_times_from_meet(url):
    """Downloads only swum times from meet excluding relay splits"""
    # Fetch meet results
    meet = fetch.fetch_meet_results(url)

    # Extract team names from URL
    names = url.split("/")[-1]
    names = names.replace("%20", " ")

    home_team = names.split(" vs ")[0]
    away_team = names.split(" vs ")[1].split(" on ")[0]

    # Extract and format date
    date = names.split(" vs ")[1].split(" on ")[1].split("?")[0]
    date = date.split("-")
    date_reformatted = "{}-{}-{}".format(
        date[2].zfill(2), date[0].zfill(2), date[1].zfill(2)
    )

    # Loop through all races
    for race in meet:

        # False because all times listed in meet results sheets are not relay splits
        # NOTE: Relay times don't count as relay splits
        is_relay_split = False
        # Add all the home times
        for home_race in race[1]:
            # Continue if empty race
            if home_race[0] == "":
                continue
            data.add_race(
                home_race[1],
                home_team,
                race[0],
                fetch.time_to_float(home_race[0]),
                home_race[0],
                date_reformatted,
                is_relay_split,
                home_race[2],
            )

        # Add all the away times
        for away_race in race[2]:
            # Continue if empty race
            if away_race[0] == "":
                continue
            data.add_race(
                away_race[1],
                away_team,
                race[0],
                fetch.time_to_float(away_race[0]),
                away_race[0],
                date_reformatted,
                is_relay_split,
                away_race[2],
            )


# data.clear_database()

#
# download_all_relays()
# data.close_connection()
