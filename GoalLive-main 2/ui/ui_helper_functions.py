import logging
import os
import time
from typing import Any

import numpy as np
import streamlit as st

# Helper functions for UI
def handle_login_success_popup() -> None:
    success_alert = st.success("Calendar fetched successfully!")
    time.sleep(5)
    success_alert.empty()


def handle_login_failed_popup(e: Exception) -> None:
    alert = st.success("Calendar fetch failed!: " + str(e))
    time.sleep(5)
    alert.empty()

def handle_application_exit(email: str) -> None:
    # delete all files inside tmp here, we do not want to store user tokens. Could have been feasible with a redis instance
    print("Quitting! See ya! :)")
    os.system(f'rm -rf ./resources/{email}.json')
    # os.kill(os.getpid(), signal.SIGTERM)
    os.system("kill -9 $(lsof -ti:8501)")

def persist_model_in_session(key: str, value: Any) -> bool:
    try:
        st.session_state[key] = value
        return True
    except Exception as e:
        logging.error(e)
        return False

def get_state_from_session(key: str) -> dict:
    return st.session_state[key]

def get_competition_key(date: str) -> str:
    return f'COMPETITIONS::{date}'

def is_key_present_in_session(key: str) -> bool:
    return key in st.session_state

def generate_random_image_url():
    random_number = np.random.randint(1, 5)
    return f"resources/f{random_number}.png"
