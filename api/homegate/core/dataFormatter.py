from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class DataFormatter():
    
    def format_data(self, dict_data: dict) -> dict:
        """Basic method to perform data cleaning on some fields and return a 
            a dict with the new fields

        Args:
            dict_data (dict): the scraped data into a dictionary

        Returns:
            dict: A dictionary with the cleaned data
        """
        data_formatted = {}
        ext_char = lambda x, changewords: re.sub(rf"({'|'.join(changewords)})", "", x)
        
        changewords = ['CHF', " ", "-", "[^\d\.]"]
        data_formatted["price_form"] = float(ext_char(dict_data["price"], changewords)) if ext_char(dict_data["price"], changewords) != '' else 0
        changewords = ['m2', " ", "[^\d\.]"]
        data_formatted["space_form"] = float(ext_char(dict_data["space"], changewords)) if ext_char(dict_data["space"], changewords) != '' else 0
        changewords = ['rm', " ", "[^\d\.]"]
        data_formatted["rooms_form"] = float(ext_char(dict_data["rooms"], changewords)) if ext_char(dict_data["rooms"], changewords) != '' else 0
        data_formatted["scrapetimeUTC"] = datetime.utcnow()
        
        return data_formatted
    
    def derive_new_fields(self, df):
        """Method that derives new fields like price per square meter and zestimage for houses"""
        df['europersqm'] = df['price_form']/df['space_form']