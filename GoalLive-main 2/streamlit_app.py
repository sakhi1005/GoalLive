import atexit

from selenium.webdriver.chrome.webdriver import WebDriver
import streamlit as st
from datetime import datetime, time
import time as tm
from streamlit import sidebar
from config.config import YELP_API_KEY, GOAL_LIVE_BASE_URL
from service.GoogleCalendarService import get_user_calendar
from ui.ui_helper_functions import handle_login_success_popup, handle_login_failed_popup, handle_application_exit, \
    persist_model_in_session, get_state_from_session, get_competition_key, is_key_present_in_session, \
    generate_random_image_url
from utils.GoogleCalendarUtils import find_free_slots_from_calendar, filter_slots_on_duration
from service.LocationService import get_user_location
from service.YelpService import YelpAPICall
from service.ScraperService import setup_headless_chrome, extract_page
from service.ScraperService import parse_html
from SlotsIntersection import filter_matches_by_user_availability

# wide space mode by default
def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

st.header("Data Focused Python Project")
st.text("Locating a suitable football match and livestream venue that accommodates your busy schedule can be a daunting task. However, we are here to assist you. Simply provide your email address, and we will retrieve your calendar and identify the most suitable options for your needs.")
# Yelp Wrapper Init
yelp_api = YelpAPICall(YELP_API_KEY)

# Streamlit Components
user_email = st.sidebar.text_input("Enter Email to fetch calendar: ")
atexit.register(handle_application_exit)
start_date = st.sidebar.date_input("Input the start date", key="start_date", format="YYYY/MM/DD")

if st.sidebar.button("Fetch Calendar"):
    try:
        user_calendar_events = get_user_calendar(user_email, start_date)
        start_of_day = datetime.combine(start_date, time.min)
        end_of_day = datetime.combine(start_date, time.max)
        user_free_slots = find_free_slots_from_calendar(start_of_day, end_of_day, user_calendar_events)
        user_free_slots = filter_slots_on_duration(user_free_slots)
        # storing user calendar
        persist_model_in_session('USER_FREE_SLOTS', user_free_slots)
        handle_login_success_popup()
    except Exception as e:
        handle_login_failed_popup(e)

if sidebar.button("Fetch Recommendations"):
    competitions = None
    with st.spinner("Cooking up options for you. Please wait..."):
        DRIVER: WebDriver = None
        USER_FREE_SLOTS = get_state_from_session('USER_FREE_SLOTS')
        setup_headless_chrome()
        start_date_in_str = start_date.strftime('%Y-%m-%d')
        if is_key_present_in_session(get_competition_key(start_date_in_str)):
            competitions = get_state_from_session(get_competition_key(start_date_in_str))
        else:
            html_source = extract_page(url = GOAL_LIVE_BASE_URL, __path=start_date_in_str)
            competitions = parse_html(html_source, date=start_date_in_str)
            persist_model_in_session(get_competition_key(start_date_in_str), competitions)
    
    competitions, time_slots = filter_matches_by_user_availability(competitions=competitions, 
                                                                   user_free_slots=USER_FREE_SLOTS)
    with st.spinner("Fetching your favourite sports destination. Smile! :)"):
        tm.sleep(2)
        latitude, longitude = get_user_location()
        yelp_response = yelp_api.call_yelp_search_api(latitude=latitude, longitude=longitude, free_slots=time_slots)

    filter_competition = lambda competitions: list(filter(lambda competition: len(competition.matches) != 0, competitions))
    competitions = filter_competition(competitions=competitions)
    competition_idx = -1
    rows, columns = len(competitions)//2, 2
        # Create the grid
    st.subheader("Competitions")
    for i in range(rows):
        # Create a row of containers
        cols = st.columns(columns)
        for j, col in enumerate(cols):
            with col:
                # Add content to each container
                with st.container():  # Create a container
                    competition_idx += 1
                    try:
                        competition = competitions[competition_idx]
                        st.subheader(f"{competition.competition_name}")
                        competition_matches = competition.matches
                        for match in competition_matches:
                            if match.home_team.team_image_url and match.away_team.team_image_url:
                                img_col1, img_col2 = st.columns(2)
                                with img_col1:
                                    st.image(match.home_team.team_image_url, width = 100)
                                with img_col2:
                                    st.image(match.away_team.team_image_url, width = 100)
                            else:
                                img_col1, img_col2 = st.columns(2)
                                # get 2 random images
                                url_1, url_2 = generate_random_image_url(), generate_random_image_url()
                                with img_col1:
                                    st.image(url_1, width = 150)
                                with img_col2:
                                    st.image(url_2, width = 150)
                            if match.home_team is not None and match.away_team is not None:
                                st.text(f"{match.home_team.team_name} VS {match.away_team.team_name}")
                            if match.match_time is not None:
                                st.text(match.match_time)

                            if match.broadcast_option:
                                st.text("Watch live broadcast at")
                                # st.write(f"{match.broadcast_option.broadcast_option_name}(%s)"%match.broadcast_option.broadcast_url)
                                st.markdown(
                                    """<a href="{}" target='_blank'>
                                    <img src={} width="50">
                                    </a>""".format(
                                        match.broadcast_option.broadcast_url + "&source=goallive",
                                        match.broadcast_option.broadcast_logo
                                    ),
                                    unsafe_allow_html=True,
                                )
                                # st.button(st.image(, width = 50), on_click=open_page, args=(match.broadcast_option.broadcast_url))
                            st.divider()
                                
                    except Exception as e:
                        print(f"COMPETITION {competition.competition_name} had issues with matches")
                        print(e)
                        continue
                
    yelp_idx = -1
    yelp_rows, yelp_columns = len(yelp_response)//2, 2
    print(f"===== YELP ROWS {yelp_rows} COLS {yelp_columns}=====")
    for i in range(yelp_rows):
        # Create a row of containers
        cols = st.columns(yelp_columns)
        for j, col in enumerate(cols):
            with col:
                yelp_idx += 1
                # Add content to each container
                try:
                    with st.container():  # Create a container (optional)
                        st.subheader("Livestream Venue Details")
                        bar_details = yelp_response[yelp_idx]
                        st.text(bar_details["name"])
                        st.text(bar_details["location"]["display_address"])
                        st.image(bar_details["image_url"])
                except Exception as e:
                    print(e)
                    continue

if st.sidebar.button("Exit"):
    handle_application_exit(user_email)
