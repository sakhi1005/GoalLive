from datetime import datetime, timedelta

from constants.ServiceabilityConstants import GAME_DURATION_IN_MINUTES, USER_EOD_TIME_IN_DATETIME, USER_START_DAY_TIME_IN_DATETIME
from dtos.FormattedCalendarEvent import FormattedCalendarEvent
from dtos.UserFreeSlot import UserFreeSlot
from utils.DateUtils import DateUtils


def format_calendar_event(event: dict) -> FormattedCalendarEvent:
    '''

    :param event: Raw event from Google Calendar API
    :return: A formatted calendar event like:
    {
        startDate: datetime
        endDate: datetime
        eventName: string
        eventDescription: string
        eventLink: string
    }
    '''

    if event is not None:
        start = event["start"].get("dateTime", event["start"].get("date"))[:-6]
        end = event["end"].get("dateTime", event["end"].get("date"))[:-6]
        start_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        end_datetime = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        eventName = event['summary']
        eventDescription = event.get('description')
        eventLink = event.get('htmlLink')

        return FormattedCalendarEvent(start_datetime, end_datetime, eventName, eventDescription, eventLink)

def get_path_to_user_account(email_id: str) -> str:
    return f"./resources/{email_id}.json"


def find_free_slots_from_calendar(start_time: datetime, end_time: datetime, calendar_events: list[FormattedCalendarEvent]) -> list[UserFreeSlot]:
    # if datetime.now() > start_time: todo put back
    #     start_time = datetime.now()

    if len(calendar_events) == 0:
        start_time = datetime.combine(start_time.date(), USER_START_DAY_TIME_IN_DATETIME.time()) + timedelta(hours=2)
        end_time = datetime.combine(end_time.date(), USER_EOD_TIME_IN_DATETIME.time()) - timedelta(hours=2)
        return [UserFreeSlot(start_time, end_time)]
    # Sort booked slots by start time
    calendar_events.sort(key=lambda x: x.start)

    calendar_events = DateUtils.filter_calendar_events_by_start_end(start_time, end_time, calendar_events)

    # Merge overlapping slots
    merged_slots = merge_overlapping_slots(calendar_events)

    # Initialize the list of free slots
    free_slots: list[UserFreeSlot] = []

    # Check for free time before the first booked slot
    if merged_slots:
        first_booked_start = merged_slots[0].start
        if start_time < first_booked_start:
            first_slot, second_slot = break_slots(start_time, first_booked_start)
            if first_slot:
                free_slots.append(first_slot)
            if second_slot:
                free_slots.append(second_slot)

    # Check for free time between booked slots
    for i in range(len(merged_slots) - 1):
        current_end = merged_slots[i].end
        next_start = merged_slots[i + 1].start
        if current_end < next_start:
            first_slot, second_slot = break_slots(current_end, next_start)
            if first_slot:
                free_slots.append(first_slot)
            if second_slot:
                free_slots.append(second_slot)

    # Check for free time after the last booked slot within the end time
    if merged_slots:
        last_booked_end = merged_slots[-1].end
        if last_booked_end < end_time:
            first_slot, second_slot = break_slots(last_booked_end, end_time)
            if first_slot:
                free_slots.append(first_slot)
            if second_slot:
                free_slots.append(second_slot)

    # Filter out any slots that start after the end time or adjust those that extend beyond it
    # free_slots = [UserFreeSlot(start, min(end, end_time)) for start, end in free_slots if start < end_time]

    # filter negative durations
    free_slots = [x for x in free_slots if x.duration > 0]

    return free_slots


def merge_overlapping_slots(booked_slots: list[FormattedCalendarEvent]):
    # Sort booked slots by start time
    booked_slots.sort(key=lambda slot: slot.start)

    merged_slots: list[FormattedCalendarEvent] = []
    for slot in booked_slots:
        if not merged_slots or merged_slots[-1].end < slot.end:
            # No overlap, add the slot as is
            merged_slots.append(slot)
        else:
            # Overlap, merge with the last slot
            merged_slots[-1].end = max(merged_slots[-1].end, slot.end)

    return merged_slots


def filter_slots_on_duration(user_slots: list[UserFreeSlot]) -> list[UserFreeSlot]:
    return [x for x in user_slots if x.duration >= GAME_DURATION_IN_MINUTES]


def break_slots(start_time: datetime, end_time: datetime) -> (UserFreeSlot, UserFreeSlot):
    '''
    - see if the current slot needs to be broken down into two slots considering out service timing
    :return: (first_slot, second_slot (if needed))
    '''
    if start_time.hour < USER_START_DAY_TIME_IN_DATETIME.hour:
        start_time = datetime.combine(start_time.date(), USER_START_DAY_TIME_IN_DATETIME.time())

    if end_time.hour > USER_EOD_TIME_IN_DATETIME.hour:
        end_time = datetime.combine(end_time.date(), USER_EOD_TIME_IN_DATETIME.time())

    return UserFreeSlot(start_time, end_time), None

