from datetime import datetime

from dtos.BroadcastOption import BroadcastOption
from dtos.Team import Team


class Match:
    def __init__(self, home_team: Team, away_team: Team, match_time: datetime, broadcast_option: BroadcastOption) -> None:
        self.home_team = home_team
        self.away_team = away_team
        self.match_time = match_time
        self.broadcast_option = broadcast_option