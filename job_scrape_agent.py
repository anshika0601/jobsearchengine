import requests
from bs4 import BeautifulSoup
import pandas as pd
import time



j=[]


url="https://internshala.com"
 
    
response=requests.get(url)
soup=BeautifulSoup(response.text,'lxml')

jobs=soup.find_all('div',class_='card')

for job in jobs:
     content=job.find('div',class_='content')
     content2=job.find('ul')
     location = "N/A"
     stipend = "N/A"
     duration = "N/A"
     if content:
        title=content.find('h4')
        company = content.find("span")
        
        
        job_title = title.text.strip() if title else "N/A"
        company_name = company.text.strip() if company else "N/A"
        
        
        
     if content2:
        li_items=content2.find_all('li')
        if len(li_items) >= 1:
            location = li_items[0].text.strip()
        
        if len(li_items) >= 2:
            stipend = li_items[1].text.strip()
        
        if len(li_items) >= 3:
            duration = li_items[2].text.strip()
            
            
        j.append({
                "Title": job_title,
                "Company": company_name,
                "Location": location,
                "Stipend": stipend, 
                "Duration": duration
                
            })
        
     
        
        
df = pd.DataFrame(j)

df.to_csv("jobs.csv", index=False)

print(df.head())
