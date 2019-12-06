class Event:
    def __init__(self, name, home_times, away_times, relay=False, diving=False):
        self.name = name
        self.home_times = home_times
        self.away_times = away_times
        self.relay = relay
        self.diving = diving

        if self.relay and self.diving:
            print("WARNING: EVENT: \"{}\" MARKED AS DIVING AND RELAY!".format(self.name))
            assert not(relay and diving)

    def score(self, display=False):
        '''Scores the event and returns in format:
        [points_home, points_away]

        '''
        points_home = 0
        points_away = 0
        # Add all times to the list
        all_times_with_dq = []
        for time in self.home_times:
            all_times_with_dq.append(['home', time])

        for time in self.away_times:
            all_times_with_dq.append(['away', time])

        all_times = []
        # Remove DQs
        for i in all_times_with_dq:
            if i[1].time == None:
                i[1].points = 0
            else:
                all_times.append(i)

        # Sort based on times
        if not(self.diving):
            all_times.sort(key=lambda x: x[1].time)
        else:
            all_times.sort(key=lambda x: x[1].time, reverse=True)






        # Set scores based on relay or not
        if self.relay:
            scores = [8, 4, 2, 0]
        else:
            scores = [6, 4, 3, 2, 1, 0]
        # if self.relay:
        #     scores = [6, 3, 1, 0]
        # else:
        #     scores = [4, 3, 1, 0, 0]

        # Add points based on times
        count = -1
        for points in scores:
            count += 1

            if len(all_times) <= count:
                break

            all_times[count][1].points = points
            if all_times[count][0] == 'home':
                points_home += points
            else:
                points_away += points

        # Print out display
        if display:
            MAX_NAME_LENGTH = 40
            lines = []

            print(self.name)
            print('-' * 10)
            for time in self.home_times:
                t = str(time)
                n = str(time.name)
                p = time.points

                lines.append('{}{}     {}{} {}    '.format(' ' * (8 - len(t)), t, n,' ' * (MAX_NAME_LENGTH - len(n)), p))

            lines.append(' ' * 35)
            lines.append(' ' * 35)
            lines.append(' ' * 35)
            count = -1
            for time in self.away_times:
                count += 1
                t = str(time)
                n = str(time.name)
                p = time.points

                # lines[count] += ('{}{}     {}{} {}'.format(' ' * (8 - len(t)), t, n,' ' * (20 - len(n)), p))
                # lines[count] += ('{0}{1}     {2}{3} {4}'.format(' ' * (8 - len(t)), t, n,' ' * (20 - len(n)), p))
                lines[count] += ('{4} {3}{2}     {1}{0}'.format(' ' * (8 - len(t)), t, n,' ' * (MAX_NAME_LENGTH - len(n)), p))

            for i in lines:
                print(i)



        print(' ' * 54, [points_home, points_away] )

        return [points_home, points_away]
