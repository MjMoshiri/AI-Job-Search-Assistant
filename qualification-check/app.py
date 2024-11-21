import requests
import dotenv
import os
import time
from openai import OpenAI
import json
from pydantic import BaseModel

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY,
)



class JobEvaluation(BaseModel):
    reasoning: str
    is_qualified: bool


def fetch_job_description(job_count):
    response = requests.get(f"http://localhost:5995/unprocessed/{job_count}")
    return response.json()


def evaluate_job(description):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": description,
            }
        ],
        response_format=JobEvaluation,
    )
    return response.choices[0].message.parsed


def process_job(job, evaluation_result):
    job["is_qualified"] = evaluation_result.is_qualified
    job["is_processed"] = True
    job["model_reasoning"] = evaluation_result.reasoning
    status = "Qualified" if job["is_qualified"] else "Not qualified"
    print(f"Job Title: {job['title']} processed. {status}. Reason: {job['model_reasoning']}")
    requests.put(f"http://localhost:5995/job/{job['id']}", json=job)
    time.sleep(0.2)


user_data = """
You will be given a job description. Review the job description and return a JSON object with two keys:
1. 'reasoning': A string providing a detailed explanation of why the job is or is not qualified based on the given conditions.
2. 'is_qualified': A boolean indicating if the job is qualified.

The qualification criteria are as follows:
- A PhD is not required.
- The role is not a management position or senior position. Which means no Senior, Director, Manager, Staff, etc. in the title.
- If a minimum experience is required, it must be less than 5 years.
- The job must be located in California or allow for remote work.

Please assess the job description carefully and ensure the reasoning covers all aspects of the criteria provided.
"""
max_attempts = 5


def process_jobs(job_count):
    while True:
        job_data = fetch_job_description(job_count)
        for job in job_data:
            job_title = job.get("title", "")
            job_description = job.get("description", "")
            attempt = 0
            while attempt < max_attempts:
                try:
                    evaluation_result = evaluate_job(
                        f'{user_data}\n ## JOB INFO ## Job Title: {job_title}\nJob Description: "{job_description}"'
                    )
                    break
                except Exception as e:
                    print(e)
                    attempt += 1
                    if attempt < max_attempts:
                        time.sleep(2)
            else:
                print("Server error. Please try again later.")
                continue

            try:
                if isinstance(evaluation_result, JobEvaluation):
                    process_job(job, evaluation_result)
                else:
                    print(
                        f"Job Title: {job_title} failed to process. Invalid response format."
                    )
            except json.JSONDecodeError:
                print(
                    f"Job Title: {job_title} failed to process. Invalid JSON response."
                )
                continue

        if len(job_data) < job_count:
            print("No more jobs to process. Exiting...")
            break


def main():
    job_count = 10
    process_jobs(job_count)


if __name__ == "__main__":
    main()
