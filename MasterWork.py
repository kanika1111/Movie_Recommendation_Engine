# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 01:32:25 2018

@author: Kanika
"""
import warnings
warnings.filterwarnings("ignore")
import DataCleaning
import MissingValueKnn as mknn
from sklearn.preprocessing import LabelEncoder
import Recommendation
# go to this page for understanding KNN regression http://www.saedsayad.com/k_nearest_neighbors_reg.htm
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
def master_work():
        dataObject=DataCleaning.DataCleaning("./movie_metadata.csv")
        dataObject.objectTypeDataCleaning()
        dataObject.garbage_clean()
        r, c = KNeighborsRegressor, KNeighborsClassifier  # Regress or classify
        title_encoder = LabelEncoder()
        title_encoder.fit(dataObject.df.movie_title)
        dataObject.df.movie_title = title_encoder.transform(dataObject.df.movie_title)
        impute_order = [('director_name', c), ('title_year', c),
                    ('actor_1_name', c), ('actor_2_name', c), ('actor_3_name', c),
                    ('gross', r), ('budget', r), ('aspect_ratio', r),
                    ('content_rating', r), ('num_critic_for_reviews', r)]
        print("COLUMN CONSIDERED NUMBER 13,14,15,16,17,18,19,20,21,22/28:-Movie IMDB LINK")
        for col, classifier in impute_order:
            dataObject.df = mknn.knn_fill(dataObject.df, col, classifier())
        titles = title_encoder.inverse_transform(dataObject.df.movie_title)
        print("Missing values filled. Data cleaning is done")
        print("Building kd tree out of dataset..")
        recommendation_engine=Recommendation.Recommendation(titles,dataObject.df.drop('movie_title', axis=1))
        print("Instance of recommendation engine is created.")
        return recommendation_engine