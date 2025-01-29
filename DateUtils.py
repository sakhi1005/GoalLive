from datetime import datetime, timedelta, time

from dtos.FormattedCalendarEvent import FormattedCalendarEvent


class DateUtils:
    @staticmethod
    def get_date_from_now(add_days: int) -> str:
        return str(datetime.today() + timedelta(days=add_days)).split()[0]

    @staticmethod
    def filter_calendar_events_by_start_end(start: datetime, end: datetime, calendar_events: list[FormattedCalendarEvent]) -> list[FormattedCalendarEvent]:
        return [x for x in calendar_events if x.start >= start and x.end <= end]

    @staticmethod
    def get_next_today_midnight() -> datetime:
        # Create a datetime object for 12 AM today
        return datetime.combine(datetime.today().date(), time(0)) + timedelta(days=1) - timedelta(hours=1)

