import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import json

# URL of the Behance profile page
url = 'https://www.behance.net/danarakhurgun1/info'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Extracting full name, job, location, followers, and bio (about section)
full_name = soup.select_one('.ProfileCard-userFullName-ule').text.strip()
job = soup.select_one('.ProfileCard-line-fVO.e2e-Profile-occupation').text.strip()
location = soup.select_one('.ProfileCard-anchor-q0M > .e2e-Profile-location').text.strip()
followers = soup.select_one('.UserInfo-statValue-d3q.e2e-UserInfo-statValue-followers-count').text.strip()
bio = soup.select_one('.UserInfo-bio-OZA').text.strip()

# Extracting links
links = {}
parent_element = soup.select_one('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC > div > div > div > div:nth-child(2) > div.UserInfo-column-ckA > div')
if parent_element:
    for link in parent_element.find_all('a'):
        domain = urlparse(link['href']).netloc.split('.')[0].capitalize()
        links[domain] = link['href']

# Extracting email addresses
all_text = soup.get_text()
emails_found = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', all_text))

# Prepare data dictionary
data = {
    "Full Name": full_name,
    "Job": job,
    "Location": location,
    "Followers": followers,
    "Bio": bio,
    "Links": links,
    "Emails": list(emails_found)
}

# Writing data to JSON file
with open('behance_profile_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data saved to behance_profile_data.json")


