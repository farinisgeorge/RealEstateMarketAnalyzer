from homegate.HGManager import HGManager


if __name__ == "__main__":
    hgmanager = HGManager()
    df = hgmanager.scrape_website()
    print(df)
