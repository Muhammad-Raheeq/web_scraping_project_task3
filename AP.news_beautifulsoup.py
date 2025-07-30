import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

results = []
for i in range(1,20):
 url = f"https://apnews.com/search?q=war&s=3&p={i}"
 resp = requests.get(url)
 

 soup = BeautifulSoup(resp.text, "html.parser")


 for item in soup.find_all(class_='PagePromo-content'):
     headline_tag = item.find(class_='PagePromo-title')
     link_tag = item.find('a')
     date_tag = item.select_one("span.Timestamp")
     desc_tag = item.find(class_="PagePromo-description")
     time_tag = item.find('bsp-timestamp')
     
     if headline_tag and desc_tag:
         headline = headline_tag.get_text(strip=True)
         link = link_tag['href'] if link_tag else "No link"
         desc = desc_tag.get_text(strip=True)
         if time_tag:
             date_str = time_tag['data-timestamp']
             date_str_2= int(date_str)
             date_have=date_str_2 / 1000
             datetime_obj = datetime.fromtimestamp(date_have)
             date=datetime_obj.date()
             results.append([headline, date, link, desc])
            

# Write to CSV
with open("apnews_war_articles.csv", mode="w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["headline","date", "url", "description"])
    writer.writerows(results)
