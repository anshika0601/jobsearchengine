import time
import csv

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException


# Edge driver path
EDGE_DRIVER_PATH = r"C:\Users\ASUS\Downloads\edgedriver_win64\msedgedriver.exe"


# Setup Edge options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

wait = WebDriverWait(driver, 20)


# Remove webdriver detection
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    },
)


# -------------------------------
# STEP 1: LOGIN
# -------------------------------

driver.get("https://www.linkedin.com/login")

print("Login to LinkedIn in the opened browser.")
input("After login press ENTER here to continue...")


# -------------------------------
# STEP 2: OPEN JOB SEARCH
# -------------------------------

search_url = "https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=India"

driver.get(search_url)

time.sleep(5)

print("Current URL:", driver.current_url)
print("Page title:", driver.title)


# -------------------------------
# STEP 3: WAIT FOR JOBS PAGE
# -------------------------------

print("\nWaiting for job list to load...")

wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".jobs-search-results-list")
    )
)
print("Current URL:", driver.current_url)
print("Page title:", driver.title)

print("Page source length:", len(driver.page_source))

# -------------------------------
# STEP 4: SCROLL JOB LIST
# -------------------------------

print("Scrolling job container...")

try:

    job_container = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")

    for i in range(25):

        driver.execute_script(
            "arguments[0].scrollBy(0, 800);",
            job_container
        )

        time.sleep(2)

        print(f"Scroll {i+1}/25")


except NoSuchElementException:

    print("Job container not found. Using window scroll...")

    for i in range(20):

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)


# -------------------------------
# STEP 5: WAIT FOR JOB CARDS
# -------------------------------

print("\nWaiting for job cards...")

wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "li.jobs-search-results__list-item")
    )
)


# -------------------------------
# STEP 6: COLLECT JOB CARDS
# -------------------------------

jobs = driver.find_elements(
    By.CSS_SELECTOR,
    "li.jobs-search-results__list-item"
)

print("\nTotal jobs detected:", len(jobs))


job_list = []


# -------------------------------
# STEP 7: EXTRACT DATA
# -------------------------------

for job in jobs:

    try:

        title_elem = job.find_element(
            By.CSS_SELECTOR,
            "a.job-card-list__title"
        )

        title = title_elem.text
        link = title_elem.get_attribute("href")


        company = "N/A"
        location = "N/A"

        try:
            company = job.find_element(
                By.CSS_SELECTOR,
                ".job-card-container__company-name"
            ).text
        except:
            pass

        try:
            location = job.find_element(
                By.CSS_SELECTOR,
                ".job-card-container__metadata-item"
            ).text
        except:
            pass


        print(f"{title} | {company} | {location}")

        job_list.append([title, company, location, link])

    except:
        continue


# -------------------------------
# STEP 8: SAVE TO CSV
# -------------------------------

if job_list:

    with open(
        "linkedin_jobs.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["Title", "Company", "Location", "Link"]
        )

        writer.writerows(job_list)

    print(f"\nSaved {len(job_list)} jobs to linkedin_jobs.csv")

else:

    print("\nNo jobs were extracted.")


# -------------------------------
# STEP 9: CLOSE
# -------------------------------

input("\nPress ENTER to close browser...")

driver.quit()