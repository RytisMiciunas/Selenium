import os
import sys
import os.path 
import random
import time
import variables as vf
import names

from phone_gen import PhoneNumber
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from pynput.keyboard import Key, Controller

def onStartSettingUpChrome():
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    driver = checkAndOpenDriver(path)
    driver.get("https://www.orioninc.com")
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, timeout=30)
    driver.implicitly_wait(3)
    return path, driver, actions, wait

def checkAndOpenDriver(path):
    pathToDriver = path +r"\chromedriver.exe"
    if(os.path.exists(pathToDriver)):
        Service_obj = Service(pathToDriver)
    else:
        raise Exception("In order to use this program you need proper path to Chrome driver")
    Service_obj = Service(pathToDriver) 
    driver = webdriver.Chrome(service=Service_obj)
    return driver

def getInformationLine():
    fullInfo = names.get_full_name().split()
    fullInfo.append(fullInfo[0] + "." + fullInfo[1] + "@gmail.com")
    phone_number = PhoneNumber("LT")
    fullInfo.append(phone_number.get_mobile())
    return fullInfo

def maximizeWindowAndAcceptCookies():
    driver.maximize_window()
    driver.find_element(By.ID, vf.acceptCookie).click()

def openCareersSection():
    careerButton = driver.find_element(By.LINK_TEXT, vf.careersButton)
    wait.until(EC.element_to_be_clickable(careerButton))
    careerButton.click()

def fillFiltersAndSearch():
    driver.find_element(By.XPATH, vf.locationDrobBox).click()
    driver.find_element(By.XPATH, vf.selectingVilnius).click()
    driver.find_element(By.XPATH, vf.categoryDropBox).click()
    driver.find_element(By.XPATH, vf.selectingSales).click()
    driver.find_element(By.CLASS_NAME, vf.searchForJobs).click()
    wait.until(EC.visibility_of_element_located((By.ID, vf.dropBoxForCategories)))

def selectAvailablePositions():
    driver.find_element(By.XPATH, vf.technologyAndEngineeringCheckBox).click()
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, vf.seniorTestAutomationEngineerPosition)))
    driver.find_element(By.PARTIAL_LINK_TEXT, vf.seniorTestAutomationEngineerPosition).click()

def openFrame():
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, vf.frameName)))
    except:
        print("Couldn't switch to frame")
    wait.until(EC.element_to_be_clickable((By.ID, vf.inputName)))

def fillInformationInForm():
    inputInformation = getInformationLine()
    driver.find_element(By.ID, vf.inputName).send_keys(inputInformation[0])
    driver.find_element(By.ID, vf.inputLastName).send_keys(inputInformation[1])
    driver.find_element(By.ID, vf.inputMail).send_keys(inputInformation[2])
    driver.find_element(By.ID, vf.inputPhone).send_keys(inputInformation[3])
    cvUpload = driver.find_element(By.XPATH, vf.uploadCv)
    coverUpload = driver.find_element(By.XPATH, vf.uploadCoverLetter)
    cvUpload.click()
    
    uploadFileFromComputer("\CV.pdf")
    wait.until(EC.element_to_be_clickable(coverUpload))
    coverUpload.click()
    uploadFileFromComputer("\cover_letter.txt")
    wait.until(EC.visibility_of_element_located((By.ID, vf.coverLetterUploadedImg)))
    driver.find_element(By.ID, vf.agreeWithPolicy).click()

def makeScreenShot():
    driver.get_screenshot_as_file("sc/screenshot.png")

def submitForm():
    driver.find_element(By.ID, vf.submitFormButton).click()

def exitChrome():
    driver.quit()

def uploadFileFromComputer(file):
    keyboard = Controller()
    time.sleep(2)
    keyboard.type(path + file)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

path, driver, actions, wait = onStartSettingUpChrome()