from homegate.core.dataScraper import DataScraper


if __name__ == "__main__":
    scraper = DataScraper(['8002', '8000'], 'buy')
    df = scraper.scrape_website()
    print(df)