import requests
from selenium import webdriver
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Fetching url
print("Press enter when the site fully loaded")

url="https://nepalipatro.com.np/gold-price-nepal"
# defining api through which data is to be extracted
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(url)
input("press enter if you entered the neccesary thing")
# collecting cookies from website 
web_cookies=driver.get_cookies()
driver.quit()
with open(f"gold_silver_complete_Rate_scrapper.csv",'w',newline="",encoding='utf-8') as f:
    writer=csv.writer(f)
    writer.writerow(["Date AD","Date_BS","Gold Price(per 10 gram)","Gold Price(per Tola)","Silver Price(Per 10 gram)","Silver Price(Per Tola)"])

# saving cookies for further processing
for i in range(5,7):
    targeted_apiurl=f"https://api.nepalipatro.com.np/v3/bullions?from-date=202{i}-1-1"
    session=requests.Session()
    for cookie in web_cookies:
        session.cookies.set(cookie['name'],cookie['value'])
    
    # defining headers
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "Accept":"application/json, text/plain, */*",
        "Referer":"https://nepalipatro.com.np/",
        "X-Requested-With": "XMLHttpRequest"
    }
    # Getting data from the api
    response=session.get(targeted_apiurl,headers=headers)
    data=response.json()
    if "data" in data:
        data=data["data"]
    print(data)
    # cleanin and saving the data in csv file
    with open(f"gold_silver_complete_Rate_scrapper.csv",'a',newline="",encoding='utf-8') as f:
        writer=csv.writer(f)
        for ad_date, values in data.items():

            writer.writerow([
                ad_date,
                values.get("bs", ""),
                values.get("g_ha", ""),
                values.get("t_ha", ""),
                values.get("g_s", ""),
                values.get("t_s", "")
            ])