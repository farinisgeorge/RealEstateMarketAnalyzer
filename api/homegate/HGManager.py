import logging
from dataclasses import dataclass, field
from api.homegate.core.dataScraper import DataScraper
from api.tools.data_uploader import DataUploader
from api.tools.postgresManager import PostgresManager


@dataclass
class HGManager:
    """
    Manager class that instantiates the needed classes to perform the data collection
    """
    zipcodes: list  = field(default_factory=lambda: [ '8002', '8005'], metadata={'choices': ['8002', '8000']})
    usage_type: str = field(default='buy', metadata={'choices': ['buy', 'rent']})
    
    def __post_init__(self):
        self.logger = logging.getLogger()
        self.scraper = DataScraper(self.zipcodes, self.usage_type)
        self.datauploader = DataUploader()
        self.postgresmanager = PostgresManager()
        
    
    def scrape_website(self):
        df = self.scraper.scrape_website()
        self.datauploader.upload_to_landing_zone(df)
        df_form = self.scraper.format_scraped_data()
        self.datauploader.upload_to_staging_zone(df_form)
        self.postgresmanager.update_postgres_data(df_form)
        return df_form