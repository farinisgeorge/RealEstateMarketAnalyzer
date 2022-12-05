import requests
import re
import json
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

city = 'austin/' #*****change this city to what you want!!!!*****

#just grabbing the first 20 pages
#feel free to make this prettier
url1 = 'https://www.zillow.com/homes/for_sale/'+city
# url2 = 'https://www.zillow.com/homes/for_sale/'+city+'/2_p/'
# url3 = 'https://www.zillow.com/homes/for_sale/'+city+'/3_p/'
# url4 = 'https://www.zillow.com/homes/for_sale/'+city+'/4_p/'
# url5 = 'https://www.zillow.com/homes/for_sale/'+city+'/5_p/'
# url6 = 'https://www.zillow.com/homes/for_sale/'+city+'/6_p/'
# url7 = 'https://www.zillow.com/homes/for_sale/'+city+'/7_p/'
# url8 = 'https://www.zillow.com/homes/for_sale/'+city+'/8_p/'
# url9 = 'https://www.zillow.com/homes/for_sale/'+city+'/9_p/'
# url10 = 'https://www.zillow.com/homes/for_sale/'+city+'/10_p/'

#add headers in case you use chromedriver (captchas are no fun); namely used for chromedriver
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

with requests.Session() as s:
    r1 = s.get(url1, headers=req_headers)
    # r2 = s.get(url2, headers=req_headers)
    # r3 = s.get(url3, headers=req_headers)
    # r4 = s.get(url4, headers=req_headers)
    # r5 = s.get(url5, headers=req_headers)
    # r6 = s.get(url6, headers=req_headers)
    # r7 = s.get(url7, headers=req_headers)
    # r8 = s.get(url8, headers=req_headers)
    # r9 = s.get(url9, headers=req_headers)
    # r10 = s.get(url10, headers=req_headers)

    data1 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r1.text).group(1))
    # data2 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r2.text).group(1))
    # data3 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r3.text).group(1))
    # data4 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r4.text).group(1))
    # data5 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r5.text).group(1))
    # data6 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r6.text).group(1))
    # data7 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r7.text).group(1))
    # data8 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r8.text).group(1))
    # data9 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r9.text).group(1))
    # data10 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r10.text).group(1))

data_list = [data1]
            # ,data11,data12,data13,data14,data15,data16,data17,data18,data19,data20]

df = pd.DataFrame()

def make_frame(frame):
    for i in data_list:
        for item in i['cat1']['searchResults']['listResults']:
            frame = frame.append(item, ignore_index=True)
    return frame

df = make_frame(df)
    
#drop cols
df = df.drop('hdpData', 1) #remove this line to see a whole bunch of other random cols, in dict format

#drop dupes
df = df.drop_duplicates(subset='zpid', keep="last")

#filters
df['zestimate'] = df['zestimate'].fillna(0)
df['best_deal'] = df['unformattedPrice'] - df['zestimate']
df = df.sort_values(by='best_deal',ascending=True)

print('shape:', df.shape)
print(df[['id','address','beds','baths','area','price','zestimate','best_deal']].head(20))