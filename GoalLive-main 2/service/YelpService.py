from datetime import datetime
import requests
from dtos.UserFreeSlot import UserFreeSlot

class YelpAPICall:
    def __init__(self, api_key):
        self.url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=10"
        self.headers = {f"accept": "application/json", "Authorization":"Bearer {}".format(api_key)}
        self.weekday_mapping = {
            "Sunday":0,
            "Monday":1,
            "Tuesday":2,
            "Wednesday":3,
            "Thursday":4,
            "Friday":5,
            "Saturday":6
        }

    def is_time_range_inside(self, start_reference_date, end_reference_date, start1, end1, start2, end2):
        """
        Check if the time range [start2, end2] on start_reference_date lies completely
        within the time range [start1, end1] on end_reference_date.
        
        Parameters:
        - start_reference_date: The date for range 2 (string in 'YYYYMMDD' format).
        - end_reference_date: The date for range 1 (string in 'YYYYMMDD' format).
        - start1, end1: Time range 1 (strings in 'HHMM' format, e.g., '0900' for 9:00 AM).
        - start2, end2: Time range 2 (strings in 'HHMM' format, e.g., '1330' for 1:30 PM).
        
        Returns:
        - True if [start2, end2] lies within [start1, end1], False otherwise.
        """
        # Combine reference dates with times to create datetime objects
        # Correct the format string to match the date format
        start1 = datetime.strptime(f"{start_reference_date} {start1[:2]}:{start1[2:]}", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime(f"{end_reference_date} {end1[:2]}:{end1[2:]}", "%Y-%m-%d %H:%M")
        start2 = datetime.strptime(f"{start_reference_date} {start2[:2]}:{start2[2:]}", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime(f"{end_reference_date} {end2[:2]}:{end2[2:]}", "%Y-%m-%d %H:%M")
        return start1 <= start2 and end2 <= end1

    def retain_unique_dicts_by_key(self, dict_list, key):
        """
        Retain unique dictionaries from a list, based on a specific key.
        
        Parameters:
        - dict_list (list): List of dictionaries.
        - key (str): Key to determine uniqueness.
        
        Returns:
        - list: List of unique dictionaries.
        """
        unique_dicts = []
        seen_keys = set()

        for d in dict_list:
            if d[key] not in seen_keys:
                unique_dicts.append(d)  # Retain the dictionary
                seen_keys.add(d[key])  # Mark the key as seen

        return unique_dicts

    def call_yelp_search_api(self, latitude: str, longitude: str, free_slots: list[UserFreeSlot]):
        bars_list = [] ## a list that will be converted to a set for getting unique restaurants.
        params = {
                'categories': 'sportsbar',
                'term': 'Sports Bar, Live Stream',
                'location': 'Pittsburgh'
                }
        response = requests.get(self.url, headers=self.headers, params=params)

        for free_slot in free_slots:
            start_time = free_slot.start_time
            end_time = free_slot.end_time
            ## need to get both start and end date as matches can go overnight on 2 different dates
            start_date = start_time.date()
            end_date = end_time.date()
            # print(response.text)
            response_businesses = response.json()['businesses']
            # print("RESPONSE BUSINESS KEYS ", response_businesses)
            start_hours = start_time.strftime("%H")       # Hours (24-hour format)
            start_minutes = start_time.strftime("%M")     # Minutes
            start_weekday = start_time.strftime("%A")     # For midnight matches, weekday can be different

            end_hours = end_time.strftime("%H")       # Hours (24-hour format)
            end_minutes = end_time.strftime("%M")     # Minutes
            end_weekday = end_time.strftime("%A")     # For midnight matches, weekday can be different

            for response_business in response_businesses: ## iterating over business responses to see if the start and end time align
                try:
                    business_hour_for_weekday_start = response_business['business_hours'][0]['open'][self.weekday_mapping[start_weekday]]['start']
                    business_hour_for_weekday_end = response_business['business_hours'][0]['open'][self.weekday_mapping[end_weekday]]['end']
                    slot_start_time, slot_end_time = start_hours+start_minutes, end_hours+end_minutes
                    if self.is_time_range_inside(start_date, end_date, business_hour_for_weekday_start, business_hour_for_weekday_end, slot_start_time, slot_end_time):
                        bars_list.append(response_business)
                except Exception as e:
                    print(response_business)
                    print(e)
                    continue
        
        id_set = self.retain_unique_dicts_by_key(bars_list, 'id')
        return id_set
            
if __name__ == "__main__":
    user_free_slots = [UserFreeSlot(datetime(2024, 11, 30, 11, 00), datetime(2024, 11, 30, 2, 00))]
    API_KEY = "idwu-jXaO-1spEHqIpUTTXd3ypT-vrtDLKLvAwwUGjpiLgOTAd1w2YMIEM1R_MjVkdv7bO5Gkr7Y7GGMvJjnxNZ409Me2KqBIy8wp-MbkkGcl38coLrLBnkWdO5IZ3Yx"
    yelp_api = YelpAPICall(API_KEY)
    restaurant_options = yelp_api.call_yelp_search_api('40.443871', '-79.944992', user_free_slots)
    print(restaurant_options)