from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from service.ElementExtractor import parse_html
from utils.DateUtils import DateUtils
from utils.UrlUtils import createURL

DRIVER: WebDriver = None
def setup_headless_chrome() -> None:
    global DRIVER
    if DRIVER is not None:
        return
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    # Additional performance and stability options
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    DRIVER.implicitly_wait(10)

def extract_page(url: str, **pathParams) -> str:
    '''

    :param url: this url should contain space for path params
    :param pathParams: key-value pairs of path params to be replaces in the url
    :return: html of the extracted page
    '''
    global DRIVER
    # Navigate to the target webpage
    processed_url = createURL(url, **pathParams)
    DRIVER.get(processed_url)

    # Wait for specific elements to load
    WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # Extract page source
    html = DRIVER.page_source

    # Close the browser
    DRIVER.quit()

    return html

if __name__ == '__main__':
    date = DateUtils.get_date_from_now(1)
    setup_headless_chrome()
    extracted_html = extract_page(url = "https://www.goal.com/en-us/fixtures/__path", __path= date)
    parse_html(extracted_html, date)





