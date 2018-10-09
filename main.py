        # -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 01:54:22 2018

@author: Kanika
"""
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, request, render_template
import tmdbsimple as tmdb
import MasterWork as mw
tmdb.API_KEY=''
search = tmdb.Search()
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    rec=re.recommend(text.split(","))
    res = []
    mo = []
    for index, movie in enumerate(rec[:6]):
        try:
            response = search.movie(query=movie)
        except:
            print("Error in connection to tmdb api, please check internet connection")  
            return render_template('index.html',name="Kanika",msg="Error in connection to tmdb api, please check internet connection")
        mo.append(movie)
        res.append("http://image.tmdb.org/t/p/w185/"+response['results'][0]['poster_path'].lstrip())
    return render_template('index.html',name="User",users=res,movie=mo)
if __name__ == "__main__":
    re=mw.master_work()
    app.run(host='127.0.0.1', port=8080)
