# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 00:56:51 2018

@author: Kanika
"""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
   #Classifier implementing the k-nearest neighbors
   #Regression based on k-nearest neighbors:-The target is predicted by local interpolation of the targets associated 
   #of the nearest neighbors in the training set.
   #Go to this page for understanding KNN classification http://www.saedsayad.com/k_nearest_neighbors.htm
   # go to this page for understanding KNN regression http://www.saedsayad.com/k_nearest_neighbors_reg.htm
def knn_fill(df, column, classifier):
    """Treat missing values as a classification / regresion problem"""
    """We are dropping the rows, who have missing values apart from the column in action"""
    ndf = df.dropna(subset=[col for col in df.columns if col != column])
    missingTargets = ndf[column].isnull()
    print("Column Considered in knn_fill", column)
    train, test  = ndf[~missingTargets], ndf[missingTargets]
    train_x, train_y = train.drop(column, axis=1), train[column]
    classifier.fit(train_x, train_y)
    if len(test) > 0:
        test_x, test_y = test.drop(column, axis=1), test[column]
        values = classifier.predict(test_x)
        test_y = values
        new_x, new_y = pd.concat([train_x, test_x]), pd.concat([train_y, test_y])
        newdf = new_x[column] = new_y
        return newdf
    else:
        return ndf
