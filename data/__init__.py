import pandas as pd

urls = pd.read_csv("urls.csv")

class find:
    def team_date(team, date):
        for index, row in urls.iterrows():
            if row[0] == date and (team.lower() == row[1].lower() or team.lower() == row[2].lower()):
                return row[3]

print(find.team_date('Cooperstown','12/5/2019'))
