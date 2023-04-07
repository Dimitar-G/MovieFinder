from SPARQLWrapper import SPARQLWrapper, TURTLE
from rdflib import Graph, URIRef


def get_movies(title):
    """
    This function queries DBpedia using SPARQL to retrieve all movies with a specified title.
    A part of the title is also efficient for the query to work.
    :param title: the title of a movie
    :return: a list with movie titles and a list of their URIs
    """

    query_string = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?movie
        WHERE {{
            ?movie foaf:name|dbp:name|rdfs:label ?title ;
            dbo:runtime ?runtime ;
            dbo:cinematography ?cinematographer .
            FILTER regex(?title, "{title}", "i") 
            FILTER (lang(?title) = 'en')
        }} LIMIT 30
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    names, uris = [], []
    for _, _, o in graph.triples((None, result_predicate, None)):
        uris.append(o)
        names.append(str(o).split('/')[-1].replace('_', ' '))

    movies_dict = {}
    for name, uri in zip(names, uris):
        movies_dict[name] = uri

    filtered_names = list(movies_dict.keys())
    filtered_uris = list(movies_dict.values())

    return filtered_names, filtered_uris


def get_directors(movie_uri):
    """
    This function queries DBpedia using SPARQL to retrieve all directors of the movie with the specified URI.
    :param movie_uri: the URI of the movie
    :return: a list of the names of all directors and a list of their URIs
    """

    query_string = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>

        SELECT ?director
        WHERE {{
            <{movie_uri}> dbo:director|dbp:director ?director .
        }}
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    directors, directors_uris = [], []
    for _, _, o in graph.triples((None, result_predicate, None)):
        directors.append(' '.join(str(o).split('/')[-1].split('_')))
        directors_uris.append(str(o))

    director_dict = {}
    for director, director_uri in zip(directors, directors_uris):
        director_dict[director] = director_uri

    filtered_directors = list(director_dict.keys())
    filtered_uris = list(director_dict.values())

    return filtered_directors, filtered_uris


def get_actors(movie_uri):
    """
    This function queries DBpedia using SPARQL to retrieve all actors starring in the movie with the specifier URI.
    :param movie_uri: the URI of the movie
    :return: a list of the names of all actors and a list of their URIs
    """

    query_string = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>

        SELECT ?actor
        WHERE {{
            <{movie_uri}> dbo:starring ?actor .
        }}
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    actors, actors_uris = [], []
    for _, _, o in graph.triples((None, result_predicate, None)):
        actors.append(' '.join(str(o).split('/')[-1].split('_')))
        actors_uris.append(o)

    actors_dict = {}
    for actor, actor_uri in zip(actors, actors_uris):
        actors_dict[actor] = actor_uri

    filtered_actors = list(actors_dict.keys())
    filtered_actors_uris = list(actors_dict.values())

    return filtered_actors, filtered_actors_uris


def get_abstract(movie_uri):
    """
    This function queries DBpedia using SPARQL to retrieve one english abstract about the movie with the specified URI.
    :param movie_uri: the URI of the movie
    :return: an abstract for the specified movie
    """

    query_string = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?abstract
        WHERE {{
            <{movie_uri}> dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }}
        LIMIT 1
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    abstract = None
    for _, _, o in graph.triples((None, result_predicate, None)):
        abstract = o
        break

    return abstract


def directed(person_uri):
    """
    This function queries DBpedia using SPARQL to retrieve all movies directed by the director that corresponds with
    the specified URI.
    :param person_uri: the URI of the director
    :return: a list of the titles of all movies directed by the specified director and a list of their URIs
    """

    query_string = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?movie
        WHERE {{
            ?movie dbo:director|dbp:director <{person_uri}> ;
            dbo:runtime ?runtime ;
            dbo:cinematography ?cinematographer .
        }}
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    names, uris = [], []
    for _, _, o in graph.triples((None, result_predicate, None)):
        uris.append(o)
        names.append(str(o).split('/')[-1].replace('_', ' '))

    movies_dict = {}
    for name, uri in zip(names, uris):
        movies_dict[name] = uri

    filtered_names = list(movies_dict.keys())
    filtered_uris = list(movies_dict.values())

    return filtered_names, filtered_uris


def starred(person_uri):
    """
    This function queries DBpedia using SPARQL to retrieve all movies starring the actor that corresponds with the
    specified URI.
    :param person_uri: the URI of the actor
    :return: a list of the titles of all movies starring the specified actor and a list of their URIs
    """

    query_string = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?movie
        WHERE {{
            ?movie dbo:starring|dbp:starring <{person_uri}> ;
            dbo:runtime ?runtime ;
            dbo:cinematography ?cinematographer .
        }}
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    names, uris = [], []
    for _, _, o in graph.triples((None, result_predicate, None)):
        uris.append(o)
        names.append(str(o).split('/')[-1].replace('_', ' '))

    movies_dict = {}
    for name, uri in zip(names, uris):
        movies_dict[name] = uri

    filtered_names = list(movies_dict.keys())
    filtered_uris = list(movies_dict.values())

    return filtered_names, filtered_uris


def get_bio(person_uri):
    """
    This function queries DBpedia to retrieve a short biography about the person that corresponds with the specified
    URI.
    :param person_uri: the URI of a person
    :return: a short biography (abstract) of the person
    """

    query_string = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?abstract
        WHERE {{
            <{person_uri}> dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }}
        LIMIT 1
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    abstract = None
    for _, _, o in graph.triples((None, result_predicate, None)):
        abstract = o
        break

    return abstract


def get_people(person_name):
    """
    This function queries DBpedia using SPARQL to retrieve all people (either actors or directors) that have a
    specified name.
    :param person_name: the name of a person
    :return: a list of the names of all people with the specified name and a list of their URIs
    """

    query_string = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?person
        WHERE {{
            ?person foaf:name|dbp:name|rdfs:label ?name .
            ?movie dbo:starring|dbp:starring|dbo:director|dbp:director ?person .
            FILTER regex(?name, "{person_name}", "i") 
            FILTER (lang(?name) = 'en')
        }}
        """

    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_string)

    results = sparql.query().convert()
    graph = Graph().parse(results)
    result_predicate = URIRef('http://www.w3.org/2005/sparql-results#value')
    names, uris = [], []
    for _, _, o in graph.triples((None, result_predicate, None)):
        uris.append(o)
        names.append(str(o).split('/')[-1].replace('_', ' '))

    people_dict = {}
    for name, uri in zip(names, uris):
        people_dict[name] = uri

    filtered_names = list(people_dict.keys())
    filtered_uris = list(people_dict.values())
    return filtered_names, filtered_uris
