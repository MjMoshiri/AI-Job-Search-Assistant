import requests
import dotenv, os
import time
dotenv.load_dotenv()
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct"
HF_TOKEN = os.getenv('HF_TOKEN')
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def fetch_job_description(job_count):
    response = requests.get(f"http://localhost:5995/unprocessed/{job_count}")
    return response.json()

def evaluate_job(description):
    payload = {
        "inputs": description,
        "parameters": {"wait_for_model": True}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    generated_text = result[0]["generated_text"]
    return generated_text

job_count = 10
while True:
    job_data = fetch_job_description(job_count)
    user_data = "Please review the job description and answer with 'Yes' if it meets all the following conditions: no PhD required, not more than 2 years of experience as a minimum, not an internship, located in California or allows remote work, and not a senior-level role. If any condition is not met, respond with 'No'. The response MUST be a single string containing either 'Yes' or 'No'."
    for job in job_data:
        job_title = job.get("title", "")
        job_description = job.get("description", "")
        evaluation_result = evaluate_job(f"{user_data})\nJob Title: {job_title}\nJob Description: {job_description} + The Answer is: ")
        answer = evaluation_result.split(":")[-1].strip()
        if answer == "Yes" or answer == "Yes.":
            job["is_qualified"] = True
            job["website"] = job.get("website", "indeed.com")
            print(f"Job Title: {job_title} processed. Qualified.")
        elif answer == "No" or answer == "No.":
            job["is_qualified"] = False
            job["website"] = job.get("website", "indeed.com")
            print(f"Job Title: {job_title} processed. Not qualified.")
        else:
            print(f"Job Title: {job_title} failed to process.{evaluation_result[-60:]}")
            continue
        response = requests.put(f"http://localhost:5995/job/{job['id']}", json=job)
        time.sleep(2.5)
    if len(job_data) < 10:
        break
