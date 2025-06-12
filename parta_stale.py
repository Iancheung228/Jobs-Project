import requests
import csv
import time
import logging

logging.basicConfig(level=logging.INFO)


APP_ID = "cf71b380"
APP_KEY = "1e7f742c34b60e970cc9ffaa6f84ba9d"
BASE_URL = "https://api.adzuna.com/v1/api/jobs/ca/search/1"

def fetch_jobs(pages=100, what = "data scientist", where = "toronto"):
    all_jobs = []
    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/ca/search/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 10,
            "what": what,
            "where": where,
            "content-type": "application/json",
            "sort_by" : "date"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            all_jobs.extend(data.get("results", []))
        except requests.RequestException as e:
            print(f"Request failed on page {page}: {e}")

        time.sleep(1)
    logging.info(f"Scraped {len(all_jobs)} jobs for '{what}' in '{where}'.")
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
