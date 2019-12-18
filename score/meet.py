class Meet:
    def __init__(self, events=None):
        if events is None:
            events = []
        self.events = events

    def score(self, display=False, entries=2):
        # Set scores to 0
        home_score = 0
        away_score = 0

        # Add scores for each event
        for e in self.events:
            points = e.score(display, entries)
            home_score += points[0]
            away_score += points[1]

        if display:
            print("Final results_array: ", home_score, away_score)
        return [home_score, away_score]
