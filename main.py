import os
import behance_scraper
import skill_extractor
import json_writer

def main():
    # List of Behance usernames
    usernames = ['danarakhurgun1', 'lanalevitann', 'jamilakhtar12']

    # Create a directory named 'data' if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    for username in usernames:
        # Construct URLs
        profile_url = f'https://www.behance.net/{username}/info'
        projects_url = f'https://www.behance.net/{username}/projects'

        # Fetch profile data
        profile_data = behance_scraper.fetch_profile_data(profile_url)

        # Fetch project links
        project_links = behance_scraper.fetch_project_links(projects_url)

        # Extract skills from projects
        skills = skill_extractor.extract_skills_from_projects(project_links)

        # Add Behance profile link to profile data
        profile_data["Behance Profile Link"] = profile_url

        # Add skills to profile data
        profile_data["Skills"] = skills

        # Save data to JSON file under 'data' folder
        json_writer.save_data_to_json(profile_data, f'data/{username}_profile_data.json')

if __name__ == "__main__":
    main()
