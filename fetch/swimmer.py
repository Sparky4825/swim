import datetime

class Swimmer:
    class Time:
        def __init__(self, name, date, time):
            self.name = name
            self.time = time
            self.date = date

        def __str__(self):
            if self.time is None:
                return 'DQ'
            time = round(self.time, 2)
            if time >= 60:
                return str(datetime.timedelta(seconds = time))[2:-4]
            else:
                return str(time)


    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.times = []
