from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import requests
import random
import json
import asyncio

BAY_AREA_URL = "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco+Bay+Area%2C+CA&radius=100&sort=date&fromage=3"
REMOTE_URL = "https://www.indeed.com/jobs?q=software+engineer&l=Remote&radius=100&sort=date&fromage=3"
EXPECTED_SAMESITE_VALUES = ["Strict", "Lax", "None"]
COOKIES_FILE = "indeed-scrapper/cookies.json"
JOB_POST_URL = "http://localhost:5995/job"


async def load_cookies(driver):
    with open(COOKIES_FILE, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            if cookie.get("sameSite") not in EXPECTED_SAMESITE_VALUES:
                cookie["sameSite"] = "None"
            await driver.add_cookie(cookie)


async def post_job(job_id, job_title, job_description, link, company, location):
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
        print("Failed to post job", response.status_code)
        return False


async def wait_for_captcha(driver):
    while True:
        title = await driver.title
        if title != "Just a moment...":
            break
        print("Please solve the captcha...")
        await driver.sleep(1)


async def scrape_jobs(driver, url):
    await driver.get("https://www.indeed.com", wait_load=True)
    await load_cookies(driver)
    await wait_for_captcha(driver)
    await driver.get(url)
    await wait_for_captcha(driver)
    failure_count = 0
    page = 0
    while True:
        try:
            await wait_for_captcha(driver)
            job_links = await driver.find_elements(By.CSS_SELECTOR, "a[data-jk]")
            for job_link in job_links:
                job_id = (await job_link.get_attribute("id")).split("_")[1]
                apply_link = f"https://www.indeed.com/applystart?jk={job_id}"
                title_element = await job_link.find_element(
                    By.CSS_SELECTOR, "span[title]"
                )
                job_title = await title_element.get_attribute("title")
                await job_link.click()
                await driver.sleep(random.randint(2, 4))
                company_element = await driver.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="inlineHeader-companyName"]'
                )
                company_name = await company_element.text
                job_description_element = await driver.find_element(
                    By.ID, "jobDescriptionText"
                )
                job_description = await job_description_element.text
                location_element = await driver.find_element(
                    By.CSS_SELECTOR,
                    'div[data-testid="inlineHeader-companyLocation"] > div',
                )
                location = await location_element.text
                success = await post_job(
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
            next_url = f"{url}&start={page * 10}"
            await driver.get(next_url, wait_load=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            return


async def main():
    options = webdriver.ChromeOptions()
    async with webdriver.Chrome(options=options) as driver:
        await scrape_jobs(driver, BAY_AREA_URL)
        await scrape_jobs(driver, REMOTE_URL)


if __name__ == "__main__":
    asyncio.run(main())
