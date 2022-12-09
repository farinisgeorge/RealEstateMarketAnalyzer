from api.homegate.HGManager import HGManager
import logging


if __name__ == "__main__":
    
    # Create `parent` logger
    logger = logging.getLogger()
    
    # Set parent's level to INFO and assign a new handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    
    logger.info("Running HomeGate Data Collector.")
    hgmanager = HGManager()
    df = hgmanager.scrape_website()
    print(df)


def main_func(zipcodes, usage_type):
    # Create `parent` logger
    logger = logging.getLogger()
    
    # Set parent's level to INFO and assign a new handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    
    logger.info("Running HomeGate Data Collector.")
    hgmanager = HGManager(zipcodes, usage_type)
    df = hgmanager.scrape_website()
    print(df)