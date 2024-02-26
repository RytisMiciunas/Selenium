import os
import sys
import os.path 
import random
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from pynput.keyboard import Key, Controller

pathToDriver = r"C:\Users\rmiciun\chromedriver-win64-122\chromedriver.exe"
if(os.path.exists(pathToDriver)):
    Service_obj = Service(pathToDriver)
else:
    raise Exception("In order to use this program you need proper path to Chrome driver")
Service_obj = Service(pathToDriver) 
driver = webdriver.Chrome(service=Service_obj)
driver.get("https://www.orioninc.com")
actions = ActionChains(driver)
wait = WebDriverWait(driver, timeout=30)
driver.implicitly_wait(3)
path = os.path.dirname(os.path.abspath(sys.argv[0]))

driver.maximize_window()
driver.find_element(By.ID,'hs-eu-confirmation-button').click()
careerButton = driver.find_element(By.LINK_TEXT, "Careers")
wait.until(EC.element_to_be_clickable(careerButton))
careerButton.click()
driver.find_element(By.XPATH, "//span[@class='label' and text()='Location']").click()
driver.find_element(By.XPATH, "//*[@id='post-108']/div/div[1]/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[10]").click()
driver.find_element(By.XPATH, "//*[@id='post-108']/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/b").click()
driver.find_element(By.XPATH, '//*[@id="post-108"]/div/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/ul/li[6]').click()
driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]").click()
wait.until(lambda x: x.find_element(By.ID, "search-filter"))
driver.find_element(By.XPATH, "//*[@id='search-filter']/div[4]/div/div[4]").click()
wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Senior')))
driver.find_element(By.PARTIAL_LINK_TEXT, 'Senior').click()
with open(path + r"\info.txt") as file:
    allLines = file.read().splitlines()
theChosenLine = random.choice(allLines)
inputInformation = theChosenLine.split()
try:
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'grnhse_iframe')))
except:
    print("Couldn't switch to frame")
wait.until(EC.element_to_be_clickable((By.ID, 'first_name')))
driver.find_element(By.ID, 'first_name').send_keys(inputInformation[0])
driver.find_element(By.ID, 'last_name').send_keys(inputInformation[1])
driver.find_element(By.ID, 'email').send_keys(inputInformation[2])
driver.find_element(By.ID, 'phone').send_keys(inputInformation[3])
cvUpload = driver.find_element(By.XPATH, '//*[@id="resume_fieldset"]/div/div[3]/button[1]')
coverUpload = driver.find_element(By.XPATH, '//*[@id="cover_letter_fieldset"]/div/div[3]/button[1]')
cvUpload.click()
time.sleep(2)
keyboard = Controller()
keyboard.type(path + r"\CV.pdf")
keyboard.press(Key.enter)
keyboard.release(Key.enter)
wait.until(EC.element_to_be_clickable(coverUpload))
coverUpload.click()
time.sleep(2)
keyboard.type(path + r"\cover_letter.txt")
keyboard.press(Key.enter)
keyboard.release(Key.enter)
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cover_letter_chosen"]/button/img')))
driver.find_element(By.XPATH, '//*[@id="data_compliance"]/div/label').click()
time.sleep(2)
driver.get_screenshot_as_file("sc/screenshot.png")
driver.find_element(By.ID, 'submit_buttons').click()