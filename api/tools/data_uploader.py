import logging
from dataclasses import dataclass, field
from azure.identity import AzureCliCredential
from azure.storage.blob import BlobServiceClient
import pandas as pd
from datetime import datetime
import pathlib
from dotenv import dotenv_values

@dataclass
class DataUploader:
    """
    Uploader class that sends data to the data lake
    """
    
    def __post_init__(self):
        self.logger = logging.getLogger()
        script_path = pathlib.Path(__file__).parent.parent.resolve()
        config = dotenv_values(f"{script_path}/configuration.env")
        
        
        self.staging_data_directory = config["staging_data_directory"]
        self.etl_container_name = config["etl_container_name"]
        self.etl_stagingarea_name = config["etl_stagingarea_name"]
        self.landing_data_directory = config["landing_data_directory"]
        self.storage_account_url = config["storage_account_url"]
        self.sql_password = config["sql_password"]
        self.sql_user = config["sql_user"]




    def upload_to_storage(self, df, data_level: str):

        """
        This will write the clean data into a csv file
        args:
        - cleaned_data: List of dictionaries of cleaned data, ready to be written into a csv file
        - data_level: The level of the data -> for example: raw, validated, access, etc.
        """
        

        # Connecting to storage account
        azure_credentials = AzureCliCredential()
        upload_file_path = rf"{data_level}\data-{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}.csv"
        blob_service_client = BlobServiceClient(f"{self.storage_account_url}",credential=azure_credentials)
        blob_client = blob_service_client.get_blob_client(
            container=self.etl_container_name, blob=upload_file_path
        )

        try:
            output = df.to_csv(index=False, sep=";", encoding="utf-8")
        except Exception as e:
            self.logger.exception(e)

        try:
            blob_client.upload_blob(output, blob_type="BlockBlob",overwrite=True)
        except Exception as e:
            self.logger.exception(e)

    
    def upload_to_landing_zone(self, df):
        self.upload_to_storage(df, self.landing_data_directory)
        
    def upload_to_staging_zone(self, df):
        self.upload_to_storage(df, self.staging_data_directory)