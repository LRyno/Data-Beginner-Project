from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(options=options, service=service)

driver.get('https://google.com')

driver.quit()    