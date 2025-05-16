import requests
from bs4 import BeautifulSoup

url = "https://www.adzuna.com/details/5130263909?utm_medium=api&utm_source=cf71b380"  # Replace with actual redirect_url

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <li> tags
    li_tags = soup.find_all("li")

    # Extract and clean bullet text
    bullet_points = [li.get_text(strip=True) for li in li_tags if len(li.get_text(strip=True)) > 5]

    if bullet_points:
        print("🔹 Responsibilities or Requirements:")
        for point in bullet_points:
            print("-", point)
    else:
        print("No bullet points found.")
else:
    print("Failed to load page:", response.status_code)
