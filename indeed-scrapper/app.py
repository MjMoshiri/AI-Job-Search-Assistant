from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import random
import json

BAY_AREA_URL = "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco+Bay+Area%2C+CA&radius=100&sort=date&fromage=3"
REMOTE_URL = "https://www.indeed.com/jobs?q=software+engineer&l=Remote&radius=100&sort=date&fromage=3"
EXPECTED_SAMESITE_VALUES = ["Strict", "Lax", "None"]
COOKIES_FILE = "indeed-scrapper/cookies.json"
JOB_POST_URL = "http://localhost:5995/job"

options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())


def load_cookies(driver):
    with open(COOKIES_FILE, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            if cookie.get("sameSite") not in EXPECTED_SAMESITE_VALUES:
                cookie["sameSite"] = "None"
            driver.add_cookie(cookie)


def post_job(job_id, job_title, job_description, link, company, location):
    job_details = {
        "id": job_id,
        "description": job_description,
        "title": job_title,
        "link": link,
        "company": company,
        "location": location,
        "is_processed": False,
    }
    response = requests.post(JOB_POST_URL, json=job_details)
    if response.status_code == 201:
        print("Job posted successfully")
        return True
    else:
        print("Failed to post job ", response.status_code)
        return False


def scrape_jobs(driver, url):
    try:
        driver.get("https://www.indeed.com")
        load_cookies(driver)
        driver.get(url)
        time.sleep(random.randint(2, 8))
        failure_count = 0
        page = 0
        while True:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a[data-jk]"))
            )
            job_links = driver.find_elements(By.CSS_SELECTOR, "a[data-jk]")
            for job_link in job_links:
                job_id = job_link.get_attribute("data-jk")
                apply_link = f"https://www.indeed.com/applystart?jk={job_id}"
                job_title = job_link.find_element(
                    By.CSS_SELECTOR, "span[title]"
                ).get_attribute("title")
                job_link.click()
                time.sleep(random.randint(2, 8))
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "jobDescriptionText"))
                )
                company_name_element = driver.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="inlineHeader-companyName"]'
                )
                company_name = company_name_element.text
                job_description = driver.find_element(By.ID, "jobDescriptionText").text

                company_location_element = driver.find_element(
                    By.CSS_SELECTOR,
                    'div[data-testid="inlineHeader-companyLocation"] > div',
                )
                location = company_location_element.text

                success = post_job(
                    job_id,
                    job_title,
                    job_description,
                    apply_link,
                    company_name,
                    location,
                )
                if not success:
                    failure_count += 1
                else:
                    failure_count = 0
                if failure_count >= 10:
                    print("Failed to post 10 jobs. Exiting...")
                    return
            page += 1
            driver.get(url + "&start=" + str(page * 10))
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    driver = webdriver.Chrome(service=service, options=options)
    try:
        # scrape_jobs(driver, BAY_AREA_URL)
        scrape_jobs(driver, REMOTE_URL)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
