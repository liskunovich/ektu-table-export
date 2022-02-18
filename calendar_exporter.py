import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

URL = 'https://calendar.google.com/calendar/u/2/r/settings/calendar/b25jZXVwb25hdGltZWluZWt0dUBnbWFpbC5jb20'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
path_for_download = os.getcwd() + "\data"


def is_file_downloaded():
    file_path = path_for_download + "\\onceuponatimeinektu@gmail.com.ical.zip"
    while not os.path.exists(file_path):
        time.sleep(2)
    if os.path.isfile(file_path):
        time.sleep(2)
        print("File Downloaded successfully..")


def log_in(driver):
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys("onceuponatimeinektu@gmail.com")
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
    time.sleep(1)
    # print('Starting input pwd')
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(
        '59"NgdSb2^#Y%`{v')
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()


def enable_download(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': path_for_download}}
    driver.execute("send_command", params)


def setting_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(f'user-agent={user_agent}')
    prefs = {'download.default_directory': path_for_download,
             "download.prompt_for_download": False}
    chrome_options.add_experimental_option("prefs", prefs)
    return chrome_options


def export():
    driver = webdriver.Chrome(options=setting_chrome_options())
    driver.get(URL)
    # print('Starting input login')
    time.sleep(1)
    log_in(driver)
    print('Starting download calendar')
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="YPCqFe"]/div/div/div/div[1]/div/div[5]/div[1]/a/span/span').click()
    is_file_downloaded()
