import flask
from flask import Flask, render_template, request
import pandas as pd
import requests
import sklearn 
import random
from sklearn.metrics.pairwise import cosine_similarity



movie_df=pd.read_csv("movie_list.csv")

from sklearn.feature_extraction.text import CountVectorizer

cv=CountVectorizer(max_features=200,stop_words="english")

vectors=cv.fit_transform(movie_df["tags"]).toarray()

similarity=cosine_similarity(vectors)

#recommender function
def fetch_movies(movie_id):
    param = {'api_key':'e226f4a5f5bace766952aa0d17182959'}  
    
    response = requests.get('https://api.themoviedb.org/3/movie/'+str(movie_id),params=param)
    data = response.json()
    poster_url="https://image.tmdb.org/t/p/w500/"+data["poster_path"]
    return poster_url



def recommend(movie_name:str):
    movie_index=movie_df[movie_df["title"]==movie_name].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:7]
    recommend_movie=[]
    recommend_movie_poster=[]
    id=[]
    for i in movie_list:
        recommend_movie.append(movie_df.iloc[i[0]].title)
        recommend_movie_poster.append(fetch_movies(movie_df.iloc[i[0]].movie_id))
        id.append("https://www.themoviedb.org/movie/"+str(movie_df.iloc[i[0]].movie_id))
    return recommend_movie,recommend_movie_poster,id
app= Flask(__name__)

@app.route("/")
def show_index():
    try:
        movieName=["The Avengers","Quantum of Solace","	Pirates of the Caribbean: On Stranger Tides","Cars 2","Transformers: Age of Extinction"]
        First_movie=random.choice(movieName)
        #query=random.choice(["The Avengers","Quantum of Solace","Pirates of the Caribbean: On Stranger Tides","Cars 2","Transformers: Age of Extinction"])
        recommend_movie,recommend_movie_poster,Id=recommend(First_movie)
    
        return render_template("index.html",page_name="SuggestMe",movie_List=recommend_movie,movie_Poster=recommend_movie_poster,movie_Id=Id,query=First_movie)
    except Exception as e:
        return render_template("index.html",page_name="SuggestMe")  




@app.route("/search",methods = ['GET'])
def search_result():
    movieName= request.args.get("Movie_query")
    try:
        recommend_movie,recommend_movie_poster,Id=recommend(movieName)
    
        return render_template("index.html",page_name="SEARCH RESULT",movie_List=recommend_movie,movie_Poster=recommend_movie_poster,movie_Id=Id)
    except Exception as e:
        print(e)
        return f"No Internet Connection{e}"

if __name__ == '__main__':
   app.run()



