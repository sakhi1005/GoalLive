from dtos.Match import Match

class Competition:
    def __init__(self, competition_name: str, matches: [Match]) -> None:
        self.competition_name = competition_name
        self.matches = matches

def filter_competitions(competitions):
    filtered_competitions = []
    for competition in competitions:
        if len(competition.matches) != 0:
            filtered_competitions.append(competition)
    return filtered_competitions