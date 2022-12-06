from dataclasses import dataclass, field
from homegate.core.dataScraper import DataScraper

@dataclass
class HGManager:
    """
    Manager class that instantiates the needed classes to perform the data collection
    """
    
    def __post_init__(self):
        self.scraper = DataScraper()
    
    def scrape_website(self):
        df = self.scraper.scrape_website()
        return df