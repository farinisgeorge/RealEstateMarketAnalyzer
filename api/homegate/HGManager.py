from dataclasses import dataclass, field
from api.homegate.core.dataScraper import DataScraper

@dataclass
class HGManager:
    """
    Manager class that instantiates the needed classes to perform the data collection
    """
    zipcodes: list  = field(default_factory=lambda: [ '8002', '8005'], metadata={'choices': ['8002', '8000']})
    usage_type: str = field(default='buy', metadata={'choices': ['buy', 'rent']})
    
    def __post_init__(self):
        self.scraper = DataScraper(self.zipcodes, self.usage_type)
    
    def scrape_website(self):
        df = self.scraper.scrape_website()
        return df