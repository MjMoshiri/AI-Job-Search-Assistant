from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, random
options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco+Bay+Area%2C+CA&sort=date"
driver.get(url)
time.sleep(random.randint(2, 8))
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-jk]')))

jobs = []

while True:
    job_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-jk]')
    for job_link in job_links:
        job_id = job_link.get_attribute('data-jk')
        job_link.click() 
        time.sleep(random.randint(2, 8))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "jobDescriptionText")))
        job_description = driver.find_element(By.ID, "jobDescriptionText").text
        jobs.append((job_id, job_description))
    try:
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')))
        next_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-jk]')))
    except Exception as e:
        print("Reached the end of the pages or an error occurred: ", e)
        break

driver.quit()
