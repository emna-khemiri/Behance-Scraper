import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def fetch_profile_data(url):
    """
    Fetches profile data from a Behance user profile URL.
    Returns a dictionary containing personal details, links, and emails.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    full_name = soup.select_one('.ProfileCard-userFullName-ule').text.strip()
    job = soup.select_one('.ProfileCard-line-fVO.e2e-Profile-occupation').text.strip()
    location = soup.select_one('.ProfileCard-anchor-q0M > .e2e-Profile-location').text.strip()
    followers = soup.select_one('.UserInfo-statValue-d3q.e2e-UserInfo-statValue-followers-count').text.strip()
    bio = soup.select_one('.UserInfo-bio-OZA').text.strip()

    # Mapping dictionary for domain labels
    domain_labels = {
        "T": "Telegram",
        # Add more mappings as needed
    }

    links = {}
    parent_element = soup.select_one('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC > div > div > div > div:nth-child(2) > div.UserInfo-column-ckA > div')
    if parent_element:
        for link in parent_element.find_all('a'):
            domain = urlparse(link['href']).netloc.split('.')[0].capitalize()
            # Check if the domain is in the mapping dictionary
            if domain in domain_labels:
                domain = domain_labels[domain]
            links[domain] = link['href']

    all_text = soup.get_text()
    emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', all_text))

    return {
        "Full Name": full_name,
        "Job": job,
        "Location": location,
        "Followers": followers,
        "Bio": bio,
        "Links": links,
        "Emails": list(emails)
    }


def fetch_project_links(url):
    """
    Fetches project links from a Behance user's projects page.
    Returns a list of project URLs.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    base_url = 'https://www.behance.net'
    project_links = soup.find_all('a', class_='ProjectCoverNeue-coverLink-U39')
    return [f'{base_url}{link.get("href")}' for link in project_links]
