from datetime import datetime

class FormattedCalendarEvent:
    def __init__(self, start: datetime, end: datetime, eventName: str, eventDescription: str, eventLink: str):
        self.start = start
        self.end = end
        self.eventName = eventName
        self.eventDescription = eventDescription
        self.eventLink = eventLink