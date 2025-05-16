import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_li_tags(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser") # creates a tree so you can search and extract elements easily
        li_tags = soup.find_all("li")
        bullets= [li.get_text(strip=True) for li in li_tags if len(li.get_text(strip=True)) > 1]

        # If no bullets found, try grabbing <p> or <br>-split text
        if not bullets:
            paragraphs = soup.find_all("p")
            for p in paragraphs:
                text = p.get_text(separator="\n", strip=True)
                lines = text.split("\n")
                bullets.extend([line for line in lines if len(line) > 10 and line.startswith("•")])

        return bullets
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def read_and_scrape(input_file="jobs_redirect.csv", output_file="responsibilities.csv"):
    with open(input_file, newline="", encoding="utf-8") as infile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["responsibilities"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            url = row["redirect_url"]
            print(f"Scraping: {url}")
            bullets = scrape_li_tags(url)
            row["responsibilities"] = " | ".join(bullets[:10])  # Limit to 10
            writer.writerow(row)
            time.sleep(1)  # Be polite

    print("✅ Scraping complete. Data saved to", output_file)

if __name__ == "__main__":
    read_and_scrape()
