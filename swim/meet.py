class Meet:
    def __init__(self, events):
        self.events = events

    def score(self, display=False):
        # Set scores to 0
        home_score = 0
        away_score = 0

        # Add scores for each event
        for e in events:
            points = e.score(display)
            home_score += points[0]
            away_score += points[1]

        return [home_score, away_score]
