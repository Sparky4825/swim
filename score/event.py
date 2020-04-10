class Event:
    def __init__(self, name, home_times, away_times, relay=False, diving=False):
        self.name = name
        self.home_times = home_times
        self.away_times = away_times
        self.relay = relay
        self.diving = diving

        if self.relay and self.diving:
            print("WARNING: EVENT: \"{}\" MARKED AS DIVING AND RELAY!".format(self.name))
            assert not (relay and diving)

    def score(self, display=False, entries=2):
        """Scores the event and returns in format:
        [points_home, points_away]"""

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
            if i[1].time is None:
                i[1].points = 0
            else:
                all_times.append(i)

        # Sort based on times
        if not self.diving:
            all_times.sort(key=lambda x: x[1].time)
        else:
            all_times.sort(key=lambda x: x[1].time, reverse=True)

        assert entries == 3 or entries == 2

        # Set scores based on relay or not
        if entries == 3:
            if self.relay:
                scores = [8, 4, 2, 0]
            else:
                scores = [6, 4, 3, 2, 1, 0]
        elif entries == 2:
            if self.relay:
                scores = [6, 3, 1, 0]
            else:
                scores = [4, 3, 1, 0, 0]
        else:
            scores = []

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
            max_name_length = 40
            lines = []

            print(self.name)
            print('-' * 10)
            for time in self.home_times:

                if not self.diving:
                    t = str(time)
                else:
                    t = '{:.2f}'.format(time.time)
                n = str(time.name)
                p = time.points

                lines.append(
                    '{}{}     {}{} {}    '.format(' ' * (8 - len(t)), t, n, ' ' * (max_name_length - len(n)), p))

            lines.append(' ' * (max_name_length + 19))
            lines.append(' ' * (max_name_length + 19))
            lines.append(' ' * (max_name_length + 19))
            count = -1
            for time in self.away_times:
                count += 1
                if not self.diving:
                    t = str(time)
                else:
                    t = '{:.2f}'.format(time.time)
                n = str(time.name)
                p = time.points

                # lines[count] += ('{}{}     {}{} {}'.format(' ' * (8 - len(t)), t, n,' ' * (20 - len(n)), p))
                # lines[count] += ('{0}{1}     {2}{3} {4}'.format(' ' * (8 - len(t)), t, n,' ' * (20 - len(n)), p))
                if count >= len(lines):
                    lines.append(' ' * (max_name_length + 19))
                lines[count] += (
                    '{4} {3}{2}     {1}{0}'.format(' ' * (8 - len(t)), t, n, ' ' * (max_name_length - len(n)), p))

            for i in lines:
                print(i)

        print(' ' * 54, [points_home, points_away])

        return [points_home, points_away]
