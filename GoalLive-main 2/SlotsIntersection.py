from datetime import datetime, timedelta
from dtos import UserFreeSlot
from tqdm import tqdm

def is_time_range_within(inner_start, inner_end, outer_start, outer_end):
    """
    Determines whether one time range lies entirely within another time range.

    Parameters:
    - inner_start (datetime): Start time of the inner time range.
    - inner_end (datetime): End time of the inner time range.
    - outer_start (datetime): Start time of the outer time range.
    - outer_end (datetime): End time of the outer time range.

    Returns:
    - bool: True if the inner time range lies entirely within the outer time range, False otherwise.
    """
    # Ensure all inputs are datetime objects
    if not all(isinstance(t, datetime) for t in [inner_start, inner_end, outer_start, outer_end]):
        raise TypeError("All inputs must be datetime objects.")

    # Check that start times are before end times
    if inner_start > inner_end:
        raise ValueError("inner_start must be earlier than inner_end.")
    if outer_start > outer_end:
        raise ValueError("outer_start must be earlier than outer_end.")

    # Determine if inner time range lies within the outer time range
    return outer_start <= inner_start and inner_end <= outer_end

def filter_matches_by_user_availability(competitions, user_free_slots):
    print("======FILTERING MATCHES======")
    """
    Filters matches within competitions based on user availability.

    Parameters:
    - competitions (list): A list of competition objects, each with a `matches` attribute containing match objects.
    - user_free_slots (list): A list of free slot objects, each with `start_time` and `end_time` attributes.
    - is_time_range_within (function): A function that checks if a time range lies within another.

    Returns:
    - list: A list of competitions with matches filtered by user availability.
    - list: A list of mutual match times that lie within the user's free slots.
    """
    mutual_match_times = []

    for competition in tqdm(competitions):  # Iterate over all competitions
        filtered_matches = []

        for match in competition.matches:  # Iterate over all matches within a competition
            try:
                # Access match start and calculate match end time
                if match.match_time is not None:
                    match_time_start = match.match_time
                    match_time_end = match_time_start + timedelta(hours=3)

                    # Check if the match falls within any of the user's free slots
                    for user_free_slot in user_free_slots:
                        user_slot_start_time = user_free_slot.start_time
                        user_slot_end_time = user_free_slot.end_time

                        if is_time_range_within(
                            inner_start=match_time_start,
                            inner_end=match_time_end,
                            outer_start=user_slot_start_time,
                            outer_end=user_slot_end_time
                        ):
                            # print("=====TIME MATCHED=======")
                            filtered_matches.append(match)
                            mutual_match_times.append(UserFreeSlot.UserFreeSlot(start_time = match_time_start,
                                                                   end_time = match_time_start + timedelta(hours=3)))
                            break ## once a match is known to be plausible, can break the loop
                        else:
                            continue
                            # print("NOT WITHIN TIME RANGE")
                            # print(f"MATCH TIME START {match_time_start} TIME END {match_time_end} \n USER TIME START {user_slot_start_time} TIME END {user_slot_end_time}")
                            # print()
            except Exception as e:
                print(f"Error processing match: {e}")
                continue

        # Update competition matches with filtered matches
        competition.matches = filtered_matches

    return competitions, mutual_match_times
    

# if __name__ == "__main__":

#     user_email = "hmulchan@andrew.cmu.edu"
#     user_calendar_events = get_user_calendar(user_email)
#     user_free_slots = find_free_slots_from_calendar(datetime.now(), datetime.now() + timedelta(hours=72), user_calendar_events)
#     user_free_slots = filter_slots_on_duration(user_free_slots)

#     DRIVER: WebDriver = None
#     setup_headless_chrome()

#     html_source = extract_page("https://www.goal.com/en-us/fixtures/2024-12-03")

#     date = DateUtils.get_date_from_now(1)
#     competitions = parse_html(html_content=html_source, date=date)
