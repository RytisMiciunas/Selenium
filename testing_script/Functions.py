import os
import sys
import os.path 
import random
import time
import variables as vf
import names
import URL

from phone_gen import PhoneNumber
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from pynput.keyboard import Key, Controller


def checkAndOpenDriver(path):
    pathToDriver = path +r"\chromedriver.exe"
    if(os.path.exists(pathToDriver)):
        Service_obj = Service(pathToDriver)
    else:
        raise Exception("In order to use this program you need proper path to Chrome driver")
    Service_obj = Service(pathToDriver) 
    driver = webdriver.Chrome(service=Service_obj)
    return driver


def onStartSettingUpChrome():
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    driver = checkAndOpenDriver(path)
    driver.get(URL.URLLink)
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, timeout=30)
    driver.implicitly_wait(3)
    return path, driver, actions, wait


def getInformationLine():
    fullInfo = names.get_full_name().split()
    fullInfo.append(fullInfo[0] + "." + fullInfo[1] + "@gmail.com")
    phone_number = PhoneNumber("LT")
    fullInfo.append(phone_number.get_mobile())
    return fullInfo


def maximizeWindowAndAcceptCookies():
    driver.maximize_window()
    driver.find_element(By.ID, vf.acceptCookieButtonId).click()


def openCareersSection():
    careerButton = driver.find_element(By.LINK_TEXT, vf.careersLinkedText)
    wait.until(EC.element_to_be_clickable(careerButton))
    careerButton.click()


def fillFiltersAndSearch():
    driver.find_element(By.XPATH, vf.locationDrobBoxXpath).click()
    driver.find_element(By.XPATH, vf.selectingVilniusXpath).click()
    driver.find_element(By.XPATH, vf.categoryDropBoxXpath).click()
    driver.find_element(By.XPATH, vf.selectingSalesXpath).click()
    driver.find_element(By.CLASS_NAME, vf.searchForJobsButtonId).click()
    wait.until(EC.visibility_of_element_located((By.ID, vf.dropBoxForCategoriesId)))

def selectAvailablePositions():
    driver.find_element(By.XPATH, vf.technologyAndEngineeringCheckBoxXpath).click()
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, vf.seniorTestAutomationEngineerPositionLinkedText)))
    driver.find_element(By.PARTIAL_LINK_TEXT, vf.seniorTestAutomationEngineerPositionLinkedText).click()

def openFrame():
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, vf.frameNameId)))
    except:
        print("Couldn't switch to frame")
    wait.until(EC.element_to_be_clickable((By.ID, vf.inputNameId)))

def fillInformationInForm():
    inputInformation = getInformationLine()
    driver.find_element(By.ID, vf.inputNameId).send_keys(inputInformation[0])
    driver.find_element(By.ID, vf.inputLastNameId).send_keys(inputInformation[1])
    driver.find_element(By.ID, vf.inputMailId).send_keys(inputInformation[2])
    driver.find_element(By.ID, vf.inputPhoneId).send_keys(inputInformation[3])
    cvUpload = driver.find_element(By.XPATH, vf.uploadCvLinkedTextXpath)
    coverUpload = driver.find_element(By.XPATH, vf.uploadCoverLetterLinkedTextXpath)
    cvUpload.click()
    
    uploadFileFromComputer("\CV.pdf")
    wait.until(EC.element_to_be_clickable(coverUpload))
    coverUpload.click()
    uploadFileFromComputer("\cover_letter.txt")
    wait.until(EC.visibility_of_element_located((By.ID, vf.coverLetterUploadedImgId)))
    driver.find_element(By.ID, vf.agreeWithPolicyCheckBoxId).click()

def makeScreenShot():
    driver.get_screenshot_as_file("sc/screenshot.png")

def submitForm():
    driver.find_element(By.ID, vf.submitFormButtonId).click()

def exitChrome():
    driver.quit()

def uploadFileFromComputer(file):
    keyboard = Controller()
    time.sleep(2)
    keyboard.type(path + file)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

path, driver, actions, wait = onStartSettingUpChrome()