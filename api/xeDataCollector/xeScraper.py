
import json
import urllib.parse
import pandas as pd
import requests
from bs4 import BeautifulSoup

postal_code_url = "https://www.xe.gr/services/places/autocomplete?query=15124&user_action=insertText&user_device=Desktop"
base_page_url = "https://www.xe.gr/property/results?transaction_name=buy&item_type=re_residence&sorting=price_per_unit_area_asc"

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
with requests.Session() as s:    
   r = s.get(postal_code_url, headers=req_headers)
   place_id = r.json()[0]["place_id"]

   base_page_content = s.get(f"{base_page_url}&geo_place_id={place_id}", headers=req_headers).content
   soup = BeautifulSoup(base_page_content, 'html.parser')

df_all = pd.DataFrame()

properties = soup.find_all(class_ = "common-property-ad")
for property_ in properties:
  df = pd.DataFrame()
  title = ",".join([p.get_text().strip() for p in property_.find_all(class_= "common-property-ad-title")])
  price = ",".join([p.get_text().replace('\n','').strip() for p in property_.find_all(class_= "common-property-ad-price")])
  price_per_sqm = ",".join([p.get_text().replace('\n','').strip() for p in property_.find_all(class_= "property-ad-price-per-sqm")])
  level = ",".join([p.get_text().strip() for p in property_.find_all(class_= "property-ad-level")])
  constr_year = ",".join([p.get_text().strip() for p in property_.find_all(class_= "xe xe-house-construction")])
  address = ",".join([p.get_text().strip() for p in property_.find_all(class_= "common-property-ad-address")])
  bedrooms = ",".join([p.get_text().strip() for p in property_.find_all(class_= "xe-bedroom")])
  bathrooms = ",".join([p.get_text().strip() for p in property_.find_all(class_= "xe-bathroom")])
  print(f"{title}|{price}|{price_per_sqm}|{level}|{constr_year}|{address}|{bedrooms}|{bathrooms}")