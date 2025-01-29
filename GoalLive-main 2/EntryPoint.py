import os
from datetime import datetime, timedelta

from service.GoogleCalendarService import get_user_calendar
import atexit

from utils.GoogleCalendarUtils import find_free_slots_from_calendar


def handle_application_exit() -> None:
    # delete all files inside tmp here, we do not want to store user tokens. Could have been feasible with a redis instance
    print("Quitting! See ya! :)")
    os.system('rm -rf ./resources/tmp/*')

if __name__ == "__main__":
    atexit.register(handle_application_exit)
    try:
        email_id = input("Enter your email id: ")
        user_calendar_events = get_user_calendar(email_id)
        print(user_calendar_events)
        # todo remove the tmp file with graceful termination of the application
        user_free_slots = find_free_slots_from_calendar(datetime.now(), datetime.now() + timedelta(hours=72), user_calendar_events)
        [print(a) for a in user_free_slots]
    except KeyboardInterrupt as error:
        handle_application_exit()
    # todo: maybe handle more exceptions