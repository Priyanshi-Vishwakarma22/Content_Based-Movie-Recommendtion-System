import os
import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    merged_data_path: str = os.path.join("artifacts", "merged_movies.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method.")

        try:
            # Load the dataset
            movies = pd.read_csv("notebook/data/tmdb_5000_movies.csv")

            credits  = pd.read_csv("notebook/data/tmdb_5000_credits.csv")

            logging.info("Datasets Loaded Successfully")

            merged_df = movies.merge(
                credits,
                on="title"
            )
            logging.info("Datasets Merged Successfully.")

            os.makedirs(
                os.path.dirname(
                    self.ingestion_config.merged_data_path
                ),
                exist_ok=True
            )

            merged_df.to_csv(
                self.ingestion_config.merged_data_path,
                index=False
            )

            
            logging.info(
                "Merged Dataset Saved Successfully"
            )

            return self.ingestion_config.merged_data_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    merged_data_path = obj.initiate_data_ingestion()
    print(merged_data_path)
        





