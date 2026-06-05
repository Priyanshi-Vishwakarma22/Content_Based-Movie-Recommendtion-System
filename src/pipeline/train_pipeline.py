from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.recommendation_engine import RecommendationEngine

from src.logger import logging

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):

        logging.info("Training Pipeline Started")

        #Data Ingestion
        ingestion_obj = DataIngestion()

        merged_path = (ingestion_obj.initiate_data_ingestion)

        # Data Transformation
        transformation_obj = DataTransformation()

        processed_path = (
            transformation_obj.initiate_data_transformation(
                merged_path
            )
        )

        # Recommendation Engine
        recommendation_obj = (
            RecommendationEngine()
        )

        recommendation_obj.initiate_recommendation_engine(
            processed_path
        )
