from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import shutil

# Try to find Edge WebDriver
edge_driver_path = None

# Option 1: Try to find in PATH
edge_driver_path = shutil.which("msedgedriver")

# Option 2: Check the Downloads folder where user extracted it
if not edge_driver_path:
    downloads_path = r"C:\Users\ASUS\Downloads\edgedriver_win64\msedgedriver.exe"
    if os.path.exists(downloads_path):
        edge_driver_path = downloads_path

# Option 3: Try common installation locations
if not edge_driver_path:
    common_paths = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "msedgedriver", "msedgedriver.exe"),
        os.path.join(os.environ.get("PROGRAMFILES", ""), "msedgedriver", "msedgedriver.exe"),
    ]
    for path in common_paths:
        if os.path.exists(path):
            edge_driver_path = path
            break

if edge_driver_path:
    print(f"Found Edge WebDriver at: {edge_driver_path}")
    driver = webdriver.Edge(service=Service(edge_driver_path))
else:
    raise Exception(
        "Edge WebDriver not found. Please either:\n"
        "1. Install msedgedriver and add it to PATH, or\n"
        "2. Download msedgedriver from https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/\n"
        "   and specify the path: webdriver.Edge(service=Service('path/to/msedgedriver.exe'))"
    )

driver.get("https://www.linkedin.com/jobs/search/?keywords=ai%20engineer")

time.sleep(5)

jobs = driver.find_elements(By.CSS_SELECTOR, "ul li[data-occludable-job-id]")
print("Total jobs found:", len(jobs))
#time.sleep(5)

#html=driver.page_source
#soup=BeautifulSoup(html,'lxml')

