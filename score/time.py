import datetime

class Time:
  def __init__(self, name, time):
    self.name = name
    self.time = time
    self.points = 0

  def __str__(self):
    time = round(self.time, 2)
    if time >= 60:
      return str(datetime.timedelta(seconds = time))[2:-4]
    else:
      return str(time)
