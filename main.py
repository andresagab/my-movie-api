from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

# APP

# create app
app = FastAPI()
# set title of app
app.title = "My app with FastAPI"
# set version
app.version = "0.0.1"

# DATA

# define movies list
movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
    },
    {
        "id": 2,
        "title": "Fast and Furios X",
        "overview": "La familia de Dom asume un nuevo reto, tras enterarse que ...",
		"year": "2023",
		"rating": 8.1,
		"category": "Acción"
    },
    {
        "id": 3,
        "title": "Avenger Infinity War",
        "overview": "Culpa et ex cillum sit deserunt irure ipsum Lorem eu.",
		"year": "2018",
		"rating": 9.8,
		"category": "Acción"
    },
    {
        "id": 4,
        "title": "Toys Story",
        "overview": "Aliquip do incididunt excepteur consectetur ad laboris velit.",
		"year": "1995",
		"rating": 8.0,
		"category": "Animación"
    },
    ]

# DEFINE ROUTES

# get /
@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

# get /movies
@app.get('/movies', tags = ['movies'])
def getMovies():
    return movies

# get /movies/{id} to search a movie by id
@app.get('/movies/{id}', tags = ['movies'])
def getMovie(id: int):
    movie = list(filter(lambda item: item['id'] == id, movies))
    if movie:
        return movie[0]
    else:
        return []
    
# get /movies => query route
@app.get('/movies/', tags = ['movies'])
def getMoviesByCategory(category: str, year: str):
    # filter movies by category or year
    result = list(filter(lambda item: category in item['category'] or year in item['year'], movies))
    if result:
        return result
    else:
        return []
    
# post /movies => to create a new movie
@app.post('/movies', tags = ['movies'])
def createMovie(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category,
    })
    return movies

# put /movies => to update a movie
@app.put('/movies/{id}', tags = ['movies'])
def updateMovie(id: int, title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    # loop movies
    for movie in movies:
        # if movie was fund by id
        if movie['id'] == id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
            break

    return movies

# delete /movies => to delete a movie
@app.delete('/movies/{id}', tags = ['movies'])
def deleteMovie(id: int):
    # loop movies
    for movie in movies:
        # if movie was fund by id
        if movie['id'] == id:
            movies.remove(movie)
            break

    return movies
