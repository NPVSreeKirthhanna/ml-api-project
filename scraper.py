import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = f"{BASE_URL}/c/courses/tools-in-data-science/67?page="
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
COOKIES = {
    "_t": "Bgv39k05gl%2BS8yT23t%2FjxG5rgQloQMZruyEvAlRrxv%2FIEAfHSBaN6CgL2b5kEFs%2F53d2heN2FrCJTLw95tC2JRT6mq0D3w2framhGzlL4IQnX4GaVYe19i%2FPChn8cxtIypt8LnM2OL2HzZI0zQmK8HGKUYKvOa%2FMyhsfVqxotvnk7N7kPaht2o%2BZds65mFT5EPdvj1Y9U1GI13j%2FUiviuO4xF%2BsOCPy30XMZ7rwPlSDzUjlF6LV%2FlyZoRcc7thzZQeTJCkuWAY7qTlRjaJsmSO%2FXrqGFezn4L67IpOnjITrYZpIkr%2FjZ6tiybaWBEwglKHPmQQ%3D%3D--mJM7kc5tT8cfoZjW--4wIIJfadTo7HoFv2vFpmzw%3D%3D"  # paste the value you copied
}

def scrape_discourse():
    posts = []
    for page in range(1, 6):  # pages 1 to 5
        print(f"Scraping page {page}...")
        url = CATEGORY_URL + str(page)
        res = requests.get(url, headers=HEADERS, cookies=COOKIES)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select('a.title.raw-link')
        if not links:
            print(f"No posts found on page {page}")
            continue
        for link in links:
            title = link.text.strip()
            post_url = BASE_URL + link["href"]
            posts.append({"title": title, "url": post_url})
    return posts

if __name__ == "__main__":
    data = scrape_discourse()
    if data:
        df = pd.DataFrame(data)
        df.to_csv("discourse_posts.csv", index=False)
        print("✅ Scraping complete. Saved to discourse_posts.csv")
    else:
        print("⚠️ No posts found. Check if the cookie has expired or is invalid.")
