import os
import sys

from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        self.movies = load_object(os.path.join("artifacts","movies.pkl"))

        self.similarity = load_object(os.path.join("artifacts","similarity.pkl"))

    
    def recommend(self, movie):
        try:
            movie_index = self.movies[self.movies["title"]==movie].index[0]

            distances = self.similarity[
                movie_index
            ]

            movies_list = sorted(
                list(enumerate(distances)),
                reverse=True,
                key=lambda x: x[1]
            )[1:6]

            recommendations = []

            for i in movies_list:
                recommendations.append(
                    self.movies.iloc[i[0]].title
                )

            return recommendations
    

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":

    obj = PredictPipeline()

    print(
        obj.recommend(
            "Avatar"
        )
    )
