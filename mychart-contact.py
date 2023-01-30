from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import creds
import time

print('\nWelcome to the Automated Gundersen Health System ® | MyChart Prescription Contact Program\n')
contact = input("Which healthcare provider would you like to contact? \'Jackie\' or \'Amelia?\': \n")
# new_message = input("What would you like to do? Type \'m\' to ask a medical question/refill prescription OR Type \'s\' to schedule an appointment")

while contact != 'Jackie' and contact != 'Amelia':
	contact = input('That healthcare provider is unknown. Please type either \'Jackie\' or \'Amelia:\'\n')

subject = input("\nEnter your subject: \n")
message = input("\nEnter your message: \n")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

username = creds.username
password = creds.password

login_url = 'https://mychart.gundersenhealth.org/MyChart/Authentication/Login?'

s = Service('/Users/jemiller/chromedriver.exe')
driver = webdriver.Chrome(service = s, options=chrome_options)

driver.get(login_url)

driver.find_element(By.NAME, 'Login').send_keys(username)
driver.find_element(By.NAME, 'Password').send_keys(password)
driver.find_element(By.ID, 'submit').send_keys(Keys.RETURN)

# Clicks the 'Messages' link at the top of landing page
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.LINK_TEXT, 'Messages'))
	)
	element.click()
except:
	driver.quit()

# Send new message
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CLASS_NAME, '_Command._actionable._command.primary.positive.sendNewMessage'))
	)
	element.click()
except:
	driver.quit()

# New Message regarding  - Ask a medical question [2]
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.CLASS_NAME, '_Command._actionable._command.Topic.selectionOption'))
	)
	element[2].click()
except:
	driver.quit()

# Prescription question [1]
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.CLASS_NAME, '_TextFragment._readOnlyText.displayName'))
	)
	element[1].click()
except:
	driver.quit()

time.sleep(3)

# Who do you want to contact? Primary care provider is [0]
def jackie():
	contact = driver.find_elements(By.CLASS_NAME, '_ListElement')[0].click()
def amelia():
	contact = driver.find_elements(By.CLASS_NAME, '_ListElement')[2].click()

if contact == 'Jackie':
	jackie()
elif contact == 'Amelia':
	amelia()
# NOTE: more names can be added from a longer list of providers

time.sleep(4)

# Subject line
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, 'EID-39'))	
	)
	element.send_keys(subject)	
except:
	driver.quit()

# Message text
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, 'EID-3a'))	
	)
	element.send_keys(message)
	print('')	
except:
	driver.quit()

# driver.quit()