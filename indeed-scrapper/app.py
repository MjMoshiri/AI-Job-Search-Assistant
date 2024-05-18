from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time, random
import json

options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
url = "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco+Bay+Area%2C+CA&sort=date"

driver.get("https://www.indeed.com")

expected_samesite_values = ["Strict", "Lax", "None"]

with open('indeed-scrapper/cookies.json', 'r') as file:
    cookies = json.load(file)
    for cookie in cookies:
        if cookie.get('sameSite') not in expected_samesite_values:
            cookie['sameSite'] = 'None'
    for cookie in cookies:
        driver.add_cookie(cookie)
        
driver.get(url)

time.sleep(random.randint(2, 8))

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-jk]"))
)

job_statuses = []

def post_job(job_id, job_title, job_description):
    job_details = {
        "id": job_id,
        "description": job_description,
        "title": job_title,
        "website": "indeed.com",
    }
    response = requests.post("http://localhost:5995/job", json=job_details)
    failure_rate = 0
    if response.status_code == 201:
        print("Job posted successfully")
        job_statuses.append(True)
    else:
        print("Failed to post job")
        job_statuses.append(False)

    if len(job_statuses) > 10:
        job_statuses.pop(0)
        failure_rate = job_statuses.count(False) / len(job_statuses)

    if failure_rate >= 0.7:
        print("Failure rate is too high. Stopping the process.")
        driver.quit()
        exit(1)
        
while True:
    job_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-jk]')
    for job_link in job_links:
        job_id = job_link.get_attribute('data-jk')
        job_title = job_link.find_element(By.CSS_SELECTOR, 'span[title]').get_attribute('title')
        job_link.click()
        time.sleep(random.randint(2, 8))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "jobDescriptionText")))
        job_description = driver.find_element(By.ID, "jobDescriptionText").text
        post_job(job_id, job_title, job_description)
    try:
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')))
        next_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-jk]')))
    except Exception as e:
        print("Reached the end of the pages or an error occurred: ", e)
        break
    
driver.quit()

