import os
import sys
import pandas as pd

from dataclasses import dataclass

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class RecommendationEngineConfig:
    movies_pkl_path = os.path.join("artifacts","movies.pkl")

    similarity_pkl_path = os.path.join("artifacts","similarity.pkl")

class RecommendationEngine:

    def __init__(self):
        self.recommendation_config = (RecommendationEngineConfig())

    def initiate_recommendation_engine(self, processed_data_path):

        try:
            logging.info("Loading processed dataset.")

            movies = pd.read_csv(processed_data_path)

            logging.info("Applying CountVectorizer")

            cv = CountVectorizer(
                max_features=5000,
                stop_words="english"
            )

            vectors = cv.fit_transform(
                movies["tags"]
            ).toarray()

            logging.info(
                "Calculating cosine similarity"
            )

            similarity = cosine_similarity(
                vectors
            )

            save_object(
                self.recommendation_config.movies_pkl_path,
                movies
            )

            save_object(
                self.recommendation_config.similarity_pkl_path,
                similarity
            )

            logging.info("Movies and similarity objects saved successfully")

            return (
                self.recommendation_config.movies_pkl_path,
                self.recommendation_config.similarity_pkl_path
            )
        
        except Exception as e:
            raise CustomException(
                e,
                sys
            )

if __name__ == "__main__":

    obj = RecommendationEngine()

    movies_path, similarity_path = (
        obj.initiate_recommendation_engine(
            "artifacts/processed_movies.csv"
        )
    )

    print(movies_path)
    print(similarity_path)    






        


