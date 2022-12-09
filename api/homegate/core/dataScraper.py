from api.homegate.core.dataFormatter import DataFormatter
from api.homegate.core.dataValidator import DataValidator

from dataclasses import dataclass, field
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pydantic import ValidationError
from time import sleep
import random
import re
import math
import logging

@dataclass
class DataScraper:
    """
    Main Scraper class for homegate website
    """
    zipcodes: list
    usage_type: str 
    
    
    def __post_init__(self):
        self.base_page_url = f"""https://www.homegate.ch/{self.usage_type}/real-estate/matching-list?loc={'%2C'.join([f"geo-zipcode-{zipc}" for zipc in self.zipcodes])}"""
        self.session = HTMLSession()
        self.df = pd.DataFrame()
        self.dataformatter = DataFormatter()
        self.logger = logging.getLogger()
    
    
    def create_soup(self, url):
        r = self.session.get(url)
        soup = BeautifulSoup(r.html.raw_html, "html.parser")
        return soup
    
        
    def get_no_pages(self, initial_soup):
        results_found =  re.sub("[^0-9]", "", initial_soup.find_all('span', attrs={"class": lambda e: e.startswith('ResultsNumber_results') if e else False })[0].get_text())
        self.no_pages = math.ceil(float(results_found)/float(20))
        self.logger.info(f"Pages Found: {self.no_pages}")
    
        
    def scrape_properties_data(self, properties):
        for property_ in properties:
        
            price =  " ".join([p.get_text().strip() for p in property_.find_all('span', attrs={"class": lambda e: e.startswith('ListItemPrice') if e else False })])
            space =  " ".join([p.get_text().strip() for p in property_.find_all('span', attrs={"class": lambda e: e.startswith('ListItemLivingSpace') if e else False })])
            rooms =  " ".join([p.get_text().strip() for p in property_.find_all('span', attrs={"class": lambda e: e.startswith('ListItemRoomNumber') if e else False })])
            item_links = property_.find_all(attrs={"class": lambda e: e.startswith('ListItem_itemLink') if e else False }, href=True)
            description =  " ".join([p.get_text().strip() for p in property_.find_all('div', attrs={"class": lambda e: e.startswith('ListItemDescription') if e else False })])

            if item_links: 
                url = f"https://www.homegate.ch{item_links[0]['href']}"
                property_id = re.sub("[^0-9]", "", item_links[0]['href'])
            elif property_['href']:
                url = f"https://www.homegate.ch{property_['href']}"
                property_id = re.sub("[^0-9]", "", property_['href'])
            else:
                url= ""
            
            new_row_dict = {
                'property_id': property_id,
                'zipcodes': ",".join(self.zipcodes),
                'usage_type': self.usage_type,
                'price': price,
                'space':space, 
                'rooms':rooms, 
                'url':url, 
                'description': description
            }
            
            new_row_dict.update(self.dataformatter.format_data(new_row_dict))
            
            try:
                row_val = DataValidator(**new_row_dict)
                new_row = pd.DataFrame(new_row_dict, index=[0])
                self.df = pd.concat([new_row,self.df.loc[:]]).reset_index(drop=True)
            except ValidationError as e:
                self.logger.exception(e)
            finally:
                pass
            
            
    
    def get_pages_data(self):
        for page in range(self.no_pages):
            router_page_url = self.base_page_url + f"&ep={page+1}"
            self.logger.info(f"In Page: {router_page_url}")
            soup = self.create_soup(router_page_url)
        
            properties =  soup.find_all(attrs={"class": lambda e: e.startswith('ResultList_ListItem') if e else False })
            self.logger.info(f"Real estates found in page: {len(properties)}")
            self.logger.info("Procceding to scraping real estates.")
            self.scrape_properties_data(properties)
            
            sleeping_time = random.uniform(3.3,10.87)
            self.logger.info(f"Sleeping for {sleeping_time} seconds...")
            sleep(sleeping_time)
            
    
    
    def scrape_website(self):
        initial_soup = self.create_soup(self.base_page_url+"&ep=1")
        self.get_no_pages(initial_soup)
        self.get_pages_data()
        
        self.logger.info("Producing new data fields.")
        self.dataformatter.derive_new_fields(self.df)
        return self.df.sort_values(by=['euro/sqm'], ignore_index=True)
        
