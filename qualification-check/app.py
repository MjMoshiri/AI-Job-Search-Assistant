import requests
import dotenv, os
import time

dotenv.load_dotenv()
API_URL = (
    "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct"
)
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def fetch_job_description(job_count):
    response = requests.get(f"http://localhost:5995/unprocessed/{job_count}")
    return response.json()


def evaluate_job(description):
    payload = {"inputs": description, "parameters": {"wait_for_model": True}}
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    generated_text = result[0]["generated_text"]
    return generated_text


def process_job(job, evaluation_result):
    job["is_qualified"] = evaluation_result == "Yes" or evaluation_result == "Yes."
    job["website"] = job.get("website", "indeed.com")
    status = "Qualified" if job["is_qualified"] else "Not qualified"
    print(f"Job Title: {job['title']} processed. {status}.")
    requests.put(f"http://localhost:5995/job/{job['id']}", json=job)
    time.sleep(2.5)


def process_jobs(job_count):
    user_data = "Please review the job description and answer with 'Yes' if it meets all the following conditions: no PhD required, not more than 2 years of experience as a minimum, located in California or allows remote work, and not a senior-level role. If any condition is not met, respond with 'No'. The response MUST be a single string containing either 'Yes' or 'No'."
    while True:
        job_data = fetch_job_description(job_count)
        for job in job_data:
            job_title = job.get("title", "")
            job_description = job.get("description", "")
            evaluation_result = evaluate_job(
                f"{user_data})\nJob Title: {job_title}\nJob Description: {job_description} + The Answer is: "
            )
            answer = evaluation_result.split(":")[-1].strip()
            if answer in ["Yes", "Yes.", "No", "No."]:
                process_job(job, answer)
            else:
                print(
                    f"Job Title: {job_title} failed to process.{evaluation_result[-60:]}"
                )
                continue
        if len(job_data) < job_count:
            break


def main():
    job_count = 10
    process_jobs(job_count)


if __name__ == "__main__":
    main()
