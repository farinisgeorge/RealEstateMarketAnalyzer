import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from time import sleep
import random
import re
import math

zipcodes = [ '8002', '8000']
usage_type = 'buy' ## buy or rent


base_page_url = f"""https://www.homegate.ch/{usage_type}/real-estate/matching-list?loc={'%2C'.join([f"geo-zipcode-{zipc}" for zipc in zipcodes])}"""

print(base_page_url)

req_headers = {  
    'authority' : 'www.homegate.ch',
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language' : 'en-US,en;q=0.9,el;q=0.8',
    'cache-control' : 'max-age=0',
    'cookie' : 'serverExperiments=NDP-652.0.PDP_OR_SRP\u0021RUB-3215.0.SRP; _mp_gen_uid=1670176027011_11615893; homegate_language=EN; homegate_language=EN; homegate_language=EN; _gcl_au=1.1.906610785.1670176028; _gid=GA1.2.1657789529.1670176028; FPLC=fzS6CPWn%2FHvSsdI9ELelANPiVRhO16AjJ2aCPSUjY0WLt3cJT9n7c%2BKBylV4cZYRHup9qMfh0SXiLdLW8%2BKGTUk7o13RKq%2FKxz2v8VDxidwAHZFSTT2SJvz%2FFetjyw%3D%3D; FPID=FPID2.2.%2B01EIHByhPzzdl62Xuwm9s5VZgShkKDPkPH3Vz6WiH4%3D.1670176028; FPAU=1.1.906610785.1670176028; _sstcl=True; _fbp=fb.1.1670176028310.3967058769; dakt_2_uuid=d7c011b6ae557636006af8552ff4f101; dakt_2_uuid_ts=1670176030256; dakt_2_version=2.1.36; ln_or=d; JSESSIONIDCMS=AA8307FE958ADE482FC664CF8D02E615; AWSALB=zLjP4Aqs1h0JZb5oVwWv7lw3gAOi0S+7GJ+mSUwnXpkEO+8aIvEy3gM9sOI0bNdA15UIs1iQJ6NXTgVNyyrtWACDdJQ+g6cZavVH2NbGOCgJhto37QaK2R5ehkrx; AWSALBCORS=zLjP4Aqs1h0JZb5oVwWv7lw3gAOi0S+7GJ+mSUwnXpkEO+8aIvEy3gM9sOI0bNdA15UIs1iQJ6NXTgVNyyrtWACDdJQ+g6cZavVH2NbGOCgJhto37QaK2R5ehkrx; _ga=GA1.2.613086869.1670176028; _uetsid=adac315073fb11edb18b1d2b62c85ca1; _uetvid=adac63d073fb11ed9fc1418a41289e94; _ga_77SLSBFELK=GS1.1.1670231096.3.1.1670232274.0.0.0',
    'sec-ch-ua' : '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile' : '?0',
    'sec-ch-ua-platform' : '"macOS"',
    'sec-fetch-dest' : 'document',
    'sec-fetch-mode' : 'navigate',
    'sec-fetch-site' : 'same-origin',
    'sec-fetch-user' : '?1',
    'upgrade-insecure-requests' : '1',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' 
}

session = HTMLSession()
r = session.get(base_page_url+"&ep=1")
soup = BeautifulSoup(r.html.raw_html, "html.parser")


df = pd.DataFrame()

results_found =  re.sub("[^0-9]", "", soup.find_all('span', attrs={"class": lambda e: e.startswith('ResultsNumber_results') if e else False })[0].get_text())
no_pages = math.ceil(float(results_found)/float(20))


for page in range(no_pages):
    
    
    router_page_url = base_page_url + f"&ep={page+1}"
    print(router_page_url)
    r = session.get(router_page_url)
    soup = BeautifulSoup(r.html.raw_html, "html.parser")
    
    properties =  soup.find_all(attrs={"class": lambda e: e.startswith('ResultList_ListItem') if e else False })
    print(len(properties))
    for property_ in properties:
        
        price =  " ".join([p.get_text().strip() for p in property_.find_all('span', attrs={"class": lambda e: e.startswith('ListItemPrice') if e else False })])
        price_formatted = re.sub("[^\d\.]", "", price)
        
        space =  " ".join([p.get_text().strip() for p in property_.find_all('span', attrs={"class": lambda e: e.startswith('ListItemLivingSpace') if e else False })])
        space_formatted = re.sub("[^\d\.]", "", space)
        rooms =  " ".join([p.get_text().strip() for p in property_.find_all('span', attrs={"class": lambda e: e.startswith('ListItemRoomNumber') if e else False })])
        rooms_formatted = re.sub("[^\d\.]", "", rooms)
        item_links = property_.find_all(attrs={"class": lambda e: e.startswith('ListItem_itemLink') if e else False }, href=True)
        if item_links: 
            url = f"https://www.homegate.ch{item_links[0]['href']}"
        elif property_['href']:
            url = f"https://www.homegate.ch{property_['href']}"
        else:
            url= ""
        
        description =  " ".join([p.get_text().strip() for p in property_.find_all('div', attrs={"class": lambda e: e.startswith('ListItemDescription') if e else False })])

        
        new_row = pd.DataFrame({'Price': price, 'Price_Form': price_formatted, 'Space':space, 'Space_Form': space_formatted, 'Rooms':rooms, 'Rooms_Form': rooms_formatted, 'Url':url, 'Description': description}, index=[0])
        df = pd.concat([new_row,df.loc[:]]).reset_index(drop=True)
    sleep(random.uniform(3.3,10.87))
    print("sleeping...")
print(df)
    