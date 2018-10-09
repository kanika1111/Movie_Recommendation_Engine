# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 00:14:40 2018

@author: Kanika
"""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
 # data processing, CSV file I/O (e.g. pd.read_csv) 
#Two-dimensional size-mutable, potentially heterogeneous tabular data structure with labeled axes (rows and columns). 
#Arithmetic operations align on both row and column labels. 
#Can be thought of as a dict-like container for Series objects. The primary pandas data structure.
class DataCleaning:
    
    def __init__(self,filepath):
        self.df = pd.read_csv(filepath)
        
    def objectTypeDataCleaning(self):
        print("#COLUMN CONSIDERED NUMBER 1/28:-COLOR")
        self.df.color = self.df.color.map({'Color': 1, ' Black and White':0})               
        #First we should know how many unique categories are there for it. we will create a set , and will iterate over the genre column.
        print("COLUMN CONSIDERED NUMBER 2/28:-GENRES")
        unique_genre_labels = set()
        for genre_flags in self.df.genres.str.split('|').values:
            unique_genre_labels = unique_genre_labels.union(set(genre_flags))
        for label in unique_genre_labels:
        #     Test if pattern or regex is contained within a string.
        # Return boolean  based on whether a given pattern or regex is contained within a string,we convert it to int via astype.
            self.df['Genre='+label] = self.df.genres.str.contains(label).astype(int)
        self.df = self.df.drop('genres', axis=1)
        print("COLUMN CONSIDERED NUMBER 3/28:-MOVIE TITLE")
        if len(self.df.drop_duplicates(subset=['movie_title',
                                      'title_year',
                                      'movie_imdb_link'])) < len(self.df):
            print('Duplicate Titles Exist')
            # Let's see these duplicates.
            # Looks like there are duplicates after all. Let's drop those.
            self.df = self.df.drop_duplicates(subset=['movie_title', 'title_year', 'movie_imdb_link'])
        print("COLUMN CONSIDERED NUMBER 4/28:-Language")
        # we can see that the language is also a value, instead of being a categorical value. We have two options either make it a
        #categorical value, or get the count and replace it with the count. As mentioned before, since most of the overvations are of
        #same type, making it a categorical value wont help.
        counts = self.df.language.value_counts()
        self.df.language = self.df.language.map(counts)
        print("COLUMN CONSIDERED NUMBER 5/28:-COUNTRY")
        count = self.df.country.value_counts()
        self.df.country = self.df.country.map(count)
        print("COLUMN CONSIDERED NUMBER 6/28:-CONTENT RATING")
        counts = self.df.content_rating.value_counts()
        self.df.content_rating = self.df.content_rating.map(counts)
        print("COLUMN CONSIDERED NUMBER 7/28:-PLOT-KEYWORDS")
        #WIll make it categorical like the genres
        unique_words = set()
        for wordlist in self.df.plot_keywords.str.split('|').values:
            if wordlist is not np.nan:
                unique_words = unique_words.union(set(wordlist))
        plot_wordbag = list(unique_words)
        for word in plot_wordbag:
            self.df['plot_has_' + word.replace(' ', '-')] = self.df.plot_keywords.str.contains(word).astype(float)
        self.df = self.df.drop('plot_keywords', axis=1)
        print("COLUMN CONSIDERED NUMBER 8/28:-Director_name")
        # We replace director name with counts of movies they've done
        self.df.director_name = self.df.director_name.map(self.df.director_name.value_counts())
        print("COLUMN CONSIDERED NUMBER 9,10,11/28:-actor_1_name,actor_2_name,actor_3_name")
        # We replace actor names with the number of movies they appear in.
        counts = pd.concat([self.df.actor_1_name, self.df.actor_2_name, self.df.actor_3_name]).value_counts()
        self.df.actor_1_name = self.df.actor_1_name.map(counts)
        self.df.actor_2_name = self.df.actor_2_name.map(counts)
        self.df.actor_3_name = self.df.actor_3_name.map(counts)

    def garbage_clean(self):
        print("COLUMN CONSIDERED NUMBER 12/28:-Movie IMDB LINK")
        # I have no clue what to do with the title. I'll keep it for now in order to search by name
        self.df = self.df.drop(['movie_imdb_link'], axis=1)
        # Let's check if anything is left as object
        print("Removing rows which have more that 100 missing values")
        self.df = self.df.dropna(thresh=100)
