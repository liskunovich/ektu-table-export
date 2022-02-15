from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome("chromedriver.exe")
driver.maximize_window()
driver.get('https://developers.google.com/calendar/api/v3/reference/calendars/clear')
wait = WebDriverWait(driver, 5)
element = wait.until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/embedded-explorer/api-method/div/div[2]/div/div[2]/form/div[1]/div[2]/div[2]/parameter/div/input')))
print(element)
element.send_keys('primary')
