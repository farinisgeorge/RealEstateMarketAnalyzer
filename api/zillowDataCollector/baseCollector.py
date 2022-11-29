from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import regex as re
import requests



request_headers = {
"accept":
"text/html, application/xhtml+xml, application/xml ;q=@.9, image/webp, image/apng, */*;q=0.8",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-US,en;q=0@.8",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.@ (Windows NT 10.0; Win64; x64) AppleWebKit/537 .36(KHTML, like Gecko) Chrome/61.0.3163.10@ Safari/537.36"
}
with requests.Session() as session:
    city = 'seattle/' #*****change this city to what you want*****
    url = 'https://www.zillow.com/homes/for_sale/' + city
    response = session.get(url, headers=request_headers)


    # add contents of urls to soup variable from each url
    soup = BeautifulSoup(response.content, "html.parser" )



    #create the first two dataframes
    df = pd.DataFrame()
    #all for loops are pulling the specified variable using beautiful soup and inserting into said variable
    for i in soup:
        address = soup.find_all (class_= 'list-card-addr' )
        price = list(soup.find_all (class_='list-card-price' ))
        beds = list(soup.find_all("ul", class_="list-card-details"))
        details = soup.find_all ("div", {'class': 'list-card-details'})
        home_type = soup.find_all ("div", {'class': 'list-card-footer'})
        last_updated = soup.find_all ("div", {'class': 'list-card-top'})
        brokerage = list(soup.find_all(class_= 'list-card-brokeragelist-card-img-overlay' , text=True) )
        link = soup.find_all (class_= 'list-card-link' )

        #create dataframe columns out of variables
        df['prices'] = price

        df['address'] = address

        df['beds'] = beds

        # convert columns to str

        df['prices'] = df['prices'].astype('str')
        df['address'] = df['address'].astype('str')
        df['beds'] = df['beds'].astype('str')

        # drop nulls
        df = df[(df['prices'] != '') & (df['prices'] !=' ')]

        # rearrange the columns
        df = df[["prices", "address", "beds"]]
    
    print(df)
