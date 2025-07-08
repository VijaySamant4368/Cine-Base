#https://github.com/LearnDataSci/articles/blob/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv

from flask import Flask, render_template, request, redirect, url_for 
from utils import getFilteredMovies, showAllMovies, getMovieDetails, getAllGenres
from findMovieIDsByDesc import getMoviesByDescText


app = Flask(__name__) 
 
# @app.route('/') 
# def home(): 
#     return render_template('index.html') 

@app.route('/submit', methods=['POST']) 
def submit(): 
    # Handle form submission 
    name = request.form.get('name') 
    return redirect(url_for('home')) 

@app.route("/", methods = ["GET", "POST"])
def movie():
    page_num = request.args.get('p', 1, type=int)
    movies, message, total_pages = getFilteredMovies(page_num=page_num)
    return render_template("movie.html", movies = movies, message=message, pageNum = page_num, totalPages = total_pages)

@app.route('/genre=<int:genre_id>')
def genre(genre_id):
    page_num = request.args.get('p', 1, type=int)
    movies, message, total_pages = getFilteredMovies(genre_ids=[genre_id], page_num=page_num)
    return render_template("movie.html", movies = movies, message=message, pageNum = page_num, totalPages = total_pages)

@app.route('/director=<int:director_id>')
def director(director_id):
    page_num = request.args.get('p', 1, type=int)
    movies, message, total_pages = getFilteredMovies(director_ids=[director_id], page_num=page_num)
    return render_template("movie.html", movies = movies, message=message, pageNum = page_num, totalPages = total_pages)

@app.route('/actor=<int:actor_id>')
def actor(actor_id):
    page_num = request.args.get('p', 1, type=int)
    movies, message, total_pages = getFilteredMovies(actor_ids=[actor_id], page_num=page_num)
    return render_template("movie.html", movies = movies, message=message, pageNum = page_num, totalPages = total_pages)

@app.route("/details=<int:movie_id>")
def details(movie_id):
    movie_details = getMovieDetails(movie_id)
    return render_template("details.html", movie = movie_details)

@app.route("/search", methods = ["GET", "POST"])
def search():
    page_num = request.args.get('p', 1, type=int)
    if request.method == 'GET':

        # grab the raw comma‑separated strings (or default to empty)
        mode = request.args.get('m', '')
        query = request.args.get('q')
        g_str = request.args.get('g', '')
        G_str = request.args.get('G', '')

        # split on commas and filter out any empty strings
        g_ids = [int(x) for x in g_str.split(',') if x]
        G_ids = [int(x) for x in G_str.split(',') if x]

        genres = getAllGenres()
        if mode == 't': #Search by Title
            movies, message, total_pages = getFilteredMovies(genre_ids=g_ids, not_genre_ids=G_ids, page_num=page_num, query=query)
        elif mode == "d":
            movie_titles = getMoviesByDescText(query)
            movies, message, total_pages = getFilteredMovies(genre_ids=g_ids, not_genre_ids=G_ids, page_num=page_num, title_ids = movie_titles)
        return render_template("search.html", genres=genres, movies = movies, message=message, totalPages = total_pages, pageNum = page_num)

if __name__ == '__main__':
    app.run(debug=True)