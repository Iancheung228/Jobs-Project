import requests
import csv
import time

APP_ID = "cf71b380"
APP_KEY = "1e7f742c34b60e970cc9ffaa6f84ba9d"
BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

def fetch_jobs(pages=1):
    all_jobs = []
    for page in range(1, pages + 1):
        url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 10,
            "what": "data scientist",
            "where": "new york",
            "content-type": "application/json"
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            all_jobs.extend(data.get("results", []))
        else:
            print(f"Error on page {page}")
        time.sleep(1)
    return all_jobs

def save_to_csv(jobs, filename="jobs_redirect.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "title", "company", "location", "category", "created",
            "contract_time", "contract_type", "salary_min", "salary_max",
            "description", "redirect_url"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs:
            writer.writerow({
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", ""),
                "location": job.get("location", {}).get("display_name", ""),
                "category": job.get("category", {}).get("label", ""),
                "created": job.get("created", ""),
                "contract_time": job.get("contract_time", ""),
                "contract_type": job.get("contract_type", ""),
                "salary_min": job.get("salary_min", ""),
                "salary_max": job.get("salary_max", ""),
                "description": job.get("description", "").replace("\n", " ").strip(),
                "redirect_url": job.get("redirect_url", "")
            })

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_to_csv(jobs)
    print("✅ Job data with redirect URLs saved.")
