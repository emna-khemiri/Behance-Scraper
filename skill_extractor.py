from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def filter_skills(skills):
    """
    Filters out any irrelevant or incorrect skill names from the list of skills.
    """
    
    # Define a list of common irrelevant words
    irrelevant_words = ['outils', 'tools', 'disciplines', 'creative fields', 'mobile', 'behance','behance mobilebehance']

    # Define specific words to categorize skills
    figma_word = 'Figma'
    procreate_word = 'Procreate'

    # Initialize a set to store filtered skills
    filtered_skills = set()

    for skill in skills:
        # Remove irrelevant words
        if skill.lower() in irrelevant_words:
            continue
        
        # Categorize skill as "Figma" if it contains the word "Figma"
        if figma_word.lower() in skill.lower():
            filtered_skills.add(figma_word)
        
        # Categorize skill as "Procreate" if it contains the word "Procreate"
        elif procreate_word.lower() in skill.lower():
            filtered_skills.add(procreate_word)
        
        # Add skill to the filtered skills set if it doesn't match specific categories
        else:
            filtered_skills.add(skill)

    return list(filtered_skills)


def extract_skills_from_projects(project_links):
    # Initialize Chrome webdriver with options
    chrome_options = Options()
    chrome_options.add_argument("--lang=en")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Set to store unique skills
    unique_skills = set()
    
    try:
        for link in project_links:
            # Load the page
            driver.get(link)

            # Wait for the skills section to be present on the page
            skills_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ProjectTools-section-k_L'))
            )

            # Extract the text from the skills section
            skills_text = skills_section.text

            # Split the text by newline character to extract individual skills
            skills = skills_text.split('\n')

            # Filter out irrelevant or incorrect skills
            filtered_skills = filter_skills(skills)

            # Add unique filtered skills to the set
            unique_skills.update(filtered_skills)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the browser
        driver.quit()

    return list(unique_skills)
