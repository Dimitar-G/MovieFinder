from flask import Flask, render_template, request
from data_functions import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')


@app.route('/movies', methods=['POST'])
def movies():
    title = request.form['title']
    title_words = title.split()
    title_words[0] = title_words[0].capitalize()
    title = ' '.join(title_words)
    movie_names, movie_uris = get_movies(title)
    return render_template('movies.html',
                           title=title,
                           movie_names_number=len(movie_names),
                           movie_names_uris=zip(movie_names, movie_uris)
                           )


@app.route('/movie')
def movie():
    movie_uri = request.args.get('uri')
    movie_title = str(movie_uri).split('/')[-1].replace('_', ' ')
    director_names, director_uris = get_directors(movie_uri)
    actor_names, actor_uris = get_actors(movie_uri)
    abstract = get_abstract(movie_uri)
    return render_template('movie.html',
                           movie_title=movie_title,
                           abstract=abstract,
                           director_names_number=len(director_names),
                           director_names_uris=zip(director_names, director_uris),
                           actor_names_number=len(actor_names),
                           actor_names_uris=zip(actor_names, actor_uris)
                           )


@app.route('/people', methods=['POST'])
def people():
    person_name = request.form['person']
    person_name = ' '.join([name.capitalize() for name in str(person_name).split()])
    people_names, people_uris = get_people(person_name)
    return render_template('people.html',
                           person_name=person_name,
                           people_names_number=len(people_names),
                           people_names_uris=zip(people_names, people_uris)
                           )


@app.route('/person')
def person():
    person_uri = request.args.get('uri')
    person_name = str(person_uri).split('/')[-1].replace('_', ' ')
    bio = get_bio(person_uri)
    directed_movie_names, directed_movie_uris = directed(person_uri)
    starred_movie_names, starred_movie_uris = starred(person_uri)
    return render_template('person.html',
                           person_name=person_name,
                           bio=bio,
                           directed_movies_number=len(directed_movie_names),
                           directed_movie_names_uris=zip(directed_movie_names, directed_movie_uris),
                           starred_movies_number=len(starred_movie_names),
                           starred_movie_names_uris=zip(starred_movie_names, starred_movie_uris)
                           )


if __name__ == '__main__':
    app.run()
