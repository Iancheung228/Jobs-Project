import requests
import csv

APP_ID = "cf71b380"
APP_KEY = "1e7f742c34b60e970cc9ffaa6f84ba9d"

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
    jobs = data.get("results", [])

    # Choose the fields you want to save
    with open("adzuna_jobs.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["title", "company", "location", "created", "salary_min", "salary_max", "description", "redirect_url"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs:
            writer.writerow({
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", ""),
                "location": job.get("location", {}).get("display_name", ""),
                "created": job.get("created", ""),
                "salary_min": job.get("salary_min", ""),
                "salary_max": job.get("salary_max", ""),
                "description": job.get("description", ""),  
                "redirect_url": job.get("redirect_url", "")
            })

    print("✅ Saved to adzuna_jobs.csv")
else:
    print("Error:", response.status_code, response.text)

# if response.status_code == 200:
#     data = response.json()
#     for job in data["results"]:
#         print(f"Title: {job['title']}")
#         print(f"Company: {job['company']['display_name']}")
#         print(f"Location: {job['location']['display_name']}")
#         print(f"Description: {job['description'][:200]}...\n")
# else:
#     print("Error:", response.status_code, response.text)
