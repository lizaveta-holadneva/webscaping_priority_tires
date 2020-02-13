# Web scaping of priority tires website
Web scarping of B2B platform Priority Tires.

Requirments file has all the libraries which should be installed. Configuration file has connection details for Redshift Database, Proxy and list of sizes for scaping.

Priority Tires website was picked up for web scraping, because it's one of the most populat B2B platforms.

Script has several loops. First loop is generating website links based on list of sizes in the configuration file. Second loop is generating page numbers from 1 to 50 (if link doesn't have products, script repeates the loop till the last 50th page). After website link has size and page information script opens Chrome browser and extract the html and javascript. Third loop is going through each card with product details and extracts necessary iformation.

### Installing
pip3 install -r requirements.txt <br>
Chrome driver: https://chromedriver.chromium.org/

### Libraries
* selenium
* bs4
* psycopg2
* requirments

### Running
python3 priority_tires.py
