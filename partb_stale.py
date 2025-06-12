import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import logging 

# function to access one redirect-url and scrape info off
def scrape_li_tags(url):
    """
    Scrapes a job description page (from Adzuna redirect URL) and extracts bullet points from <li> or fallback to <p>/<br>.
    
    Parameters:
        url (str): The redirect URL to scrape.
    
    Returns:
        list: A list of extracted bullet points (strings).
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, "html.parser") # creates a tree so you can search and extract elements easily

        for tag in soup(["script", "style", "meta", "noscript"]):
            tag.decompose()

        # Try <li> tags first
        li_tags = soup.find_all("li")
        bullets = [li.get_text(strip=True) for li in li_tags if len(li.get_text(strip=True)) > 3]

        # If no bullets found, try grabbing <p> or <br>-split text
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text = p.get_text(separator="\n", strip=True)
            if len(text) > 15:
                bullets.append(text)

        sections = soup.find_all("section")

        for section in sections:
            text = section.get_text(separator=" ", strip=True)
            if len(text) >= 1000:
                bullets.append(text)

        
        return bullets
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []


def read_and_scrape(input_file="jobs_redirect.csv", output_file="responsibilities.csv", max_bullets=10):
    """
    Reads a CSV of job postings, scrapes responsibilities from each job page, and writes to a new CSV.

    Parameters:
        input_file (str): Input CSV file with redirect URLs.
        output_file (str): Output CSV file with scraped responsibilities.
        max_bullets (int): Max number of bullet points to include per job.
    """
    non_empty_res = 0
    with open(input_file, newline="", encoding="utf-8") as infile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["responsibilities"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            raw_url = row.get("redirect_url", "")
            url = convert_to_details_url(raw_url)
            if not url:
                print(f"⚠️ Skipping missing URL for row: {row.get('title')}")
                continue

            print(f"🔍 Scraping: {url}")
            bullets = scrape_li_tags(url)  # Assuming you're now using the improved scraper

            if bullets:
                
                row["responsibilities"] = " | ".join(bullets[:])
                non_empty_res += 1
            else:
                row["responsibilities"] = ""

            writer.writerow(row)
            time.sleep(1)  # Rate-limiting to avoid being blocked

    print(f"✅ Scraping complete. Data saved to: {output_file}")
    logging.info(f"📝 Total jobs with non-empty responsibilities: {non_empty_res}")


def convert_to_details_url(landing_url):
    # Extract job ID from the landing URL
    match = re.search(r'/land/ad/(\d+)', landing_url)
    if match:
        job_id = match.group(1)
        return f"https://www.adzuna.com/details/{job_id}"
    return landing_url  # fallback

if __name__ == "__main__":
    read_and_scrape()


