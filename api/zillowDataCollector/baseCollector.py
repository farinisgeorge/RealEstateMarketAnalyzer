import requests
import re
import json
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

city = 'nashville/' #*****change this city to what you want!!!!*****

#just grabbing the first 20 pages
#feel free to make this prettier
url1 = 'https://www.zillow.com/homes/for_sale/'+city
url2 = 'https://www.zillow.com/homes/for_sale/'+city+'/2_p/'
url3 = 'https://www.zillow.com/homes/for_sale/'+city+'/3_p/'
url4 = 'https://www.zillow.com/homes/for_sale/'+city+'/4_p/'
url5 = 'https://www.zillow.com/homes/for_sale/'+city+'/5_p/'
url6 = 'https://www.zillow.com/homes/for_sale/'+city+'/6_p/'
url7 = 'https://www.zillow.com/homes/for_sale/'+city+'/7_p/'
url8 = 'https://www.zillow.com/homes/for_sale/'+city+'/8_p/'
url9 = 'https://www.zillow.com/homes/for_sale/'+city+'/9_p/'
url10 = 'https://www.zillow.com/homes/for_sale/'+city+'/10_p/'

#add headers in case you use chromedriver (captchas are no fun); namely used for chromedriver
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}