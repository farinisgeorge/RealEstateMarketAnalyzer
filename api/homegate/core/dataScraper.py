from dataclasses import dataclass, field
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from time import sleep
import random
import re
import math

@dataclass
class DataScraper:
    """
    Main Scraper class for homegate website
    """
    zipcodes: list  = field(default_factory=['8002', '8000'], metadata={'choices': ['8002', '8000']})
    usage_type: str = field(default='buy', metadata={'choices': ['buy', 'rent']})
    
    
    def __post_init__(self):
        self.base_page_url = f"""https://www.homegate.ch/{self.usage_type}/real-estate/matching-list?loc={'%2C'.join([f"geo-zipcode-{zipc}" for zipc in self.zipcodes])}"""
        print(self.base_page_url)
        self.session = HTMLSession()
        self.df = pd.DataFrame()
    
    
    def create_soup(self, url):  
        r = self.session.get(url)
        soup = BeautifulSoup(r.html.raw_html, "html.parser")
        return soup
    
        
    def get_no_pages(self, initial_soup):
        results_found =  re.sub("[^0-9]", "", initial_soup.find_all('span', attrs={"class": lambda e: e.startswith('ResultsNumber_results') if e else False })[0].get_text())
        self.no_pages = math.ceil(float(results_found)/float(20))
    
        
    def scrape_properties_data(self, properties):
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
            self.df = pd.concat([new_row,self.df.loc[:]]).reset_index(drop=True)
        
    
    def get_pages_data(self):
        for page in range(self.no_pages):
            router_page_url = self.base_page_url + f"&ep={page+1}"
            print(router_page_url)
            soup = self.create_soup(router_page_url)
        
            properties =  soup.find_all(attrs={"class": lambda e: e.startswith('ResultList_ListItem') if e else False })
            print(len(properties))
            self.scrape_properties_data(properties)
            
            sleep(random.uniform(3.3,10.87))
            print("sleeping...")
    
    
    def scrape_website(self):
        initial_soup = self.create_soup(self.base_page_url+"&ep=1")
        self.get_no_pages(initial_soup)
        self.get_pages_data()
        return self.df
        
