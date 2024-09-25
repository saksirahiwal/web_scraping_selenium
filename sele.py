from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Define the website and path to chromedriver
website = 'https://www.adamchoi.co.uk/overs/detailed'
path = r'C:\web Scrapping(1)\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Ensure correct path

# Create a Service object for chromedriver
service = Service(executable_path=path)

# Start the Chrome WebDriver using the Service object
driver = webdriver.Chrome(service=service)

# Open the website
driver.get(website)

# Wait until the 'All matches' button is visible and click it
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//label[@analytics-event="All matches"]')))
    all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
    all_matches_button.click()
except Exception as e:
    print(f"Error locating or clicking 'All matches' button: {e}")
    driver.quit()

# Wait for the table to load
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
except Exception as e:
    print(f"Error loading table: {e}")
    driver.quit()

# Locate the table that contains the match data
table = driver.find_element(By.TAG_NAME, 'table')

# Find all rows ('tr' elements) within the table
matches = table.find_elements(By.TAG_NAME, 'tr')

# Lists to hold the table data
date = []
home_team = []
score = []
away_team = []

# Iterate over each match (row)
for match in matches:
    try:
        # Get all 'td' elements in each row
        cells = match.find_elements(By.TAG_NAME, 'td')
        
        if len(cells) >= 4:  # Ensure there are at least 4 'td' elements in the row
            date.append(cells[0].text)         # Date column
            home_team.append(cells[1].text)    # Home team column
            score.append(cells[2].text)        # Score column
            away_team.append(cells[3].text)    # Away team column
        else:
            print("Skipping row due to insufficient data.")
    except Exception as e:
        print(f"Error processing row: {e}")
        continue

# Create a DataFrame from the lists
df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})

# Save DataFrame to a CSV file
df.to_csv('football_data.csv', index=False)

# Print the DataFrame
print(df)

# Quit the driver
driver.quit()
