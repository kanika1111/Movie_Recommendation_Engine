# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 01:03:59 2018

@author: Kanika
"""
import warnings
warnings.filterwarnings("ignore")
from sklearn.neighbors import KDTree
from sklearn.preprocessing import MinMaxScaler
class Recommendation:
    def __init__(self,titles,data):
        self.titles=titles
        self.data=MinMaxScaler().fit_transform(data)
        self.tree= KDTree(self.data, leaf_size=3)
        self.movies=[]
        
    def recommend(self,names):
        self._get_movies(names)
        """
        Recommend movies on the basis of the KDTree generated.
        Return them in order of increasing distance form knowns.
        """
        self.titles = list(self.titles)
        length, recommendations = len(self.movies) + 1,[]
        
        for i, movie in enumerate(self.movies):
            weight = length - i
            dist, index = self.tree.query([self.data[self.titles.index(movie)]], k=5)
            print("dist",dist,"index",index)
            for d, m in zip(dist[0], index[0]):
                 recommendations.append((d*weight, self.titles[m]))
        recommendations.sort()
        rec = [i[1].strip() for i in recommendations]
        return rec
    
    def _get_movies(self,names):
        self.movies=[]
        for name in names:
            found = [i for i in self.titles if name.lower() in i.lower()]
            if len(found) > 0:
                self.movies.append(found[0])
    