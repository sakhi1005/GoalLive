from datetime import datetime

from utils.DateUtils import DateUtils

GAME_DURATION_IN_MINUTES = 90
# dummy year, month, day
USER_EOD_TIME_IN_DATETIME = DateUtils.get_next_today_midnight()
USER_START_DAY_TIME_IN_DATETIME = datetime(year=2024, month=1, day=1, hour=10, minute=0, second=0)