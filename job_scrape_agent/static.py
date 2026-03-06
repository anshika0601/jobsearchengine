import requests
from bs4 import BeautifulSoup
import csv
import time

for i in range(1, 5):
     if i==1:
      url= "https://internshala.com/jobs/bigbrand-true/"
     else:   
       url = f"https://internshala.com/jobs/bigbrand-true/page-{i}"
     response = requests.get(url)
     soup = BeautifulSoup(response.text, "lxml")
     main_container = soup.find("div", id="internship_list_container")
     cards = main_container.find_all("div", class_="individual_internship")
     jobs=[]
     for card in cards:
         title = card.select_one("h3.job-internship-name a")
         company = card.select_one("p.company-name")
         location = card.select_one(".row-1-item.locations span")
         stipend = card.select_one("div.row-1-item span")
        
         job_data= {
            "Title": title.text.strip() if title else "N/A",
            "Company": company.text.strip() if company else "N/A",
            "Location": location.text.strip() if location else "N/A",
            "Stipend": stipend.text.strip() if stipend else "N/A"
        }
         jobs.append(job_data)
     time.sleep(2)    
        

keys = jobs[0].keys()

with open("internships_dataset.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(jobs)

print("Dataset saved!")