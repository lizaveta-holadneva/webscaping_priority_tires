import requests
import re
import psycopg2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, timedelta, datetime

#Connect to the database
from configurations import(PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD, PG_PORT, PROXY, sizes_list)
conn=psycopg2.connect(dbname=PG_DATABASE, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
cur=conn.cursor()
now = datetime.now()
datetime=now.strftime("%Y-%m-%d %H:%M:%S")

#Parameters for Proxy, would be used in the loop
webdriver.DesiredCapabilities.CHROME['proxy']={
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "autodetect":False
}

#Splitting link to be able to go through page numbers and list of sizes
#https://www.prioritytire.com/search.php#/filter:ss_size:195$253E65$253E15
first_part="https://www.prioritytire.com/search.php"
page_number="?p="
second_part="#/filter:ss_size:"
width="$253E"
sidewall="$253E"

#base_url=str(first_part)+str(second_part)

for u in sizes_list:
    r = u.split('-')
    #url_size=str(first_part)+str(page_number)+str(page)+str(second_part)+r[0]+str(width)+r[1]+str(sidewall)+r[2]
    #print(url)
    for page in range(1,50,1):
        #Open links in chrome without oppening the browser
        url=str(first_part)+str(page_number)+str(page)+str(second_part)+r[0]+str(width)+r[1]+str(sidewall)+r[2]
        print(url)
        options = Options()
        options.headless=True
        #Use Proxy
        options.add_argument('--proxy-server=%s' % PROXY)
        #Chrome driver
        #Install and search for the driver in the code https://intellipaat.com/community/15101/selenium-chromedriver-executable-needs-to-be-in-path
        path="/Users/lizavetaholadneva/Desktop/Python/web_scaping/chromedriver" #Should be modified by the link provided before or driver should be downloaded and new path should be created
        driver = webdriver.Chrome(path, options=options)
        driver.get(url)
        #Takes entire script including html and javascript
        html = driver.execute_script("return document.documentElement.outerHTML")
        sel_soup = BeautifulSoup(html,"html.parser")

        all=sel_soup.find_all("li",{"class":"product ng-scope"})

        #Loop to scrape all information from the link
        for item in all:
            #Main Information
            brand=item.find("span",{"class":"card_brand ng-binding"}).text

            model_name=item.find("span",{"class":"pro_model_name ng-binding"}).text

            season=item.find("span",{"class":"performance_txt ng-binding ng-scope"}).text

            size=item.find("span",{"class":"product_sku ng-binding"}).text.split("\t")[0].replace(" ","")

            load_speed=item.find("span",{"class":"product_sku ng-binding"}).text.split("\t")[7].replace(" ","")

            sku=str(size+" "+load_speed)

            speed_index=re.sub(r"^.*\d","",load_speed)

            load_index=re.sub(r"[A-Z]+","",load_speed)

            price=item.find("span",{"class":"price price--withoutTax ng-binding"}).text

            full_stock=item.find("div",{"class":"stock_level ng-binding"}).text.replace("\t","")
            stock=re.sub(r"\D+","",full_stock)

            #Spacifications
            load_range=item.find_all("span",{"class":"ctm_value ng-binding ng-scope"})[1].text
            try:
                run_flat=item.find_all("span",{"class":"ctm_value ng-binding ng-scope"})[3].text
            except:
                run_flat="No"
            try:
                tread_life=item.find_all("span",{"class":"ctm_value ng-binding ng-scope"})[2].text
            except:
                tread_life="None"

            #Additional data
            timestamp=datetime
            id=str(timestamp+"_"+sku)
            source="priority_tire"

            #Insert data
            query="INSERT INTO websites_data (id, timestamp, brand, model_name, season, size, sku, speed_index, load_index, price, stock, load_range, run_flat, tread_life, source) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data=(id, timestamp, brand, model_name, season, size, sku, speed_index, load_index, price, stock, load_range, run_flat, tread_life, source)
            cur.execute(query, data)
            #If link doesn't have product iformation than script will break.
            
            print(data)

    if str(all) !='[]':
        print("Infomation is available") 
    else:
        break
            

conn.commit()