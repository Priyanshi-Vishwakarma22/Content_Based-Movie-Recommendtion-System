import os
from pydoc import text
import sys
import ast
import pandas as pd

from dataclasses import dataclass

from nltk.stem.porter import PorterStemmer
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    processed_data_path = os.path.join("artifacts", "processed_movies.csv")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.ps = PorterStemmer()

# Helper Functions
    # Genres & Keywords
    def convert(self, obj):
        L = []

        for i in ast.literal_eval(obj):
            L.append(i["name"])

        return L
    
    # Cast
    def convert_cast(self, obj):
        L = []
        counter = 0

        for i in ast.literal_eval(obj):

            if counter != 3:
                L.append(i['name'])
                counter += 1
            else:
                break

        return L
    
    # Director
    def fetch_director(self, obj):
        L = []

        for i in ast.literal_eval(obj):
            if i["job"] == "Director":
                L.append(i["name"])
                break
        return L
        
    # Stemming
    def stem(self, text):
        y = []
        
        for i in text.split():
            y.append(self.ps.stem(i))
        return " ".join(y)
    
    def initiate_data_transformation(self, data_path):
        try:
            movies = pd.read_csv(data_path)
            logging.info("Dataset Loaded")

            # Genres & Keywords
            movies["genres"] = movies["genres"].apply(self.convert)
            movies["keywords"] = movies["keywords"].apply(self.convert)

             # Cast
            movies["cast"] = movies["cast"].apply(
                self.convert_cast
            )

            # Director
            movies["crew"] = movies["crew"].apply(
                self.fetch_director
            )

            # Overview Split
            movies["overview"] = movies["overview"].apply(
                lambda x: x.split()
            )

            # Remove Spaces
            movies["genres"] = movies["genres"].apply(
                lambda x: [i.replace(" ", "") for i in x]
            )

            movies["keywords"] = movies["keywords"].apply(
                lambda x: [i.replace(" ", "") for i in x]
            )

            movies["cast"] = movies["cast"].apply(
                lambda x: [i.replace(" ", "") for i in x]
            )

            movies["crew"] = movies["crew"].apply(
                lambda x: [i.replace(" ", "") for i in x]
            )


            # Create Tags
            movies["tags"] = (
                movies["overview"]
                + movies["genres"]
                + movies["keywords"]
                + movies["cast"]
                + movies["crew"]
            )


            new_df = movies[
                [
                    "movie_id",
                    "title",
                    "tags"
                ]
            ].copy()

             # Text Normalization
            new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))
            new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

             # Stemming
            new_df["tags"] = new_df["tags"].apply(self.stem)

            #Save folder
            os.makedirs(
                os.path.dirname(self.data_transformation_config.processed_data_path),
                exist_ok=True
            )

            new_df.to_csv(
                self.data_transformation_config.processed_data_path,
                index=False
            )

            logging.info("Processed dataset saved successfully")

            return self.data_transformation_config.processed_data_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    obj = DataTransformation()
    processed_path = obj.initiate_data_transformation(
        "notebook/data/cleaned_movies.csv"
    )
    print(processed_path)










        



    

