import psycopg2
from sqlalchemy import create_engine
import sqlalchemy
from dataclasses import dataclass, field
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import pandas as pd
from datetime import datetime
import pathlib
from dotenv import dotenv_values
import logging

@dataclass
class PostgresManager:
    """
    Uploader class that sends data to the Postgres Database
    """
    
    def __post_init__(self):
        self.logger = logging.getLogger()
        script_path = pathlib.Path(__file__).parent.parent.resolve()
        config = dotenv_values(f"{script_path}/configuration.env")
        
        self.table_name = config["table_name"]
        dbname = config["dbname"]
        user = config["user"]
        password = config["password"]
        host = config["host"]
        
        
        self.staging_data_directory = config["staging_data_directory"]
        self.etl_container_name = config["etl_container_name"]
        self.etl_stagingarea_name = config["etl_stagingarea_name"]
        self.landing_data_directory = config["landing_data_directory"]
        self.storage_account_url = config["storage_account_url"]
        self.sql_password = config["sql_password"]
        self.sql_user = config["sql_user"]
        
        self.conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host = host,
        port = "5432"
        )
        
        self.engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{dbname}")
        self.conn.autocommit = True
        




    def create_table(self):

        try:
            cursor = self.create_tableconn.cursor()
            sql = f'''CREATE TABLE IF NOT EXISTS {self.table_name} ( \
                    property_id VARCHAR(255), \
                    zipcodes VARCHAR(255), \
                    usage_type VARCHAR(255), \
                    price VARCHAR(255), \
                    space VARCHAR(255), \
                    rooms VARCHAR(255), \
                    url VARCHAR(255), \
                    description VARCHAR(255), \
                    price_form NUMERIC(6,2), \
                    space_form NUMERIC(6,2), \
                    rooms_form NUMERIC(6,2), \
                    europersqm NUMERIC(6,2), \
                    scrapetimeUTC DATE, \
                    key SERIAL PRIMARY KEY, \
                    );
                    '''
            cursor.execute(sql)
            self.logger.info(f"Table {self.table_name} created succesfully........")
        
        except Exception as e:
            self.logger.info("""
            --------------------------------------------------------
            |An error ocurred. Check the logs for more information.|
            --------------------------------------------------------
            """)
            
        finally:
            self.conn.close()


    def insert_data_into_table(self, df):
        
        df.to_sql(f"{self.table_name}",con=self.engine,if_exists="append",index=False)

        self.logger.info(f"Data copied to {self.table_name}........")
    
        
    def update_postgres_data(self, df):
        self.create_table()
        self.insert_data_into_table(df)