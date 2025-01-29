from datetime import datetime


class UserFreeSlot:
    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.duration: int = (end_time - start_time).total_seconds() // 60