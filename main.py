from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request
from jwt_manager import create_token, valid_token
from fastapi.security import HTTPBearer

# APP

# create app
app = FastAPI()
# set title of app
app.title = "My app with FastAPI"
# set version
app.version = "0.0.1"

# DATA

# define class JWTBearer
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # get user credential
        auth = await super().__call__(request)
        # valid token with user credential
        data: dict = valid_token(auth.credentials)
        # valid credentials
        if data['email'] != "admin@admin.com":
            # generate HTTP exception
            raise HTTPException(status_code = 403, detail = "Invalid credentials")


# define schema of users
class User(BaseModel):
    email:str
    password: str

# define schema of movie
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length = 5, max_length = 15)
    overview: str = Field(min_length = 15, max_length = 50)
    year: str= Field(min_length = 4, max_length = 4)
    rating: float = Field(ge = 1, le = 10)
    category: str = Field(min_length = 5, max_length = 15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My movie",
                "overview": "Description movie",
                "year": "2023",
                "rating": 8.5,
                "category": "Category movie",
            }
        }


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

# post /login => to authenticate user
@app.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        # call to create token sending user convert to dict
        token: str = create_token(user.dict())
        # return JSON response with status code and token
        return JSONResponse(status_code = 200, content = token)
    return user

# get /movies => return JSONResponse
@app.get('/movies', tags = ['movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    return JSONResponse(status_code = 200, content = movies)

# get /movies/{id} to search a movie by id, and valid param with path
@app.get('/movies/{id}', tags = ['movies'], response_model = Movie)
def getMovie(id: int = Path(ge = 1, le = 2000)) -> Movie:
    movie = list(filter(lambda item: item['id'] == id, movies))
    if movie:
        return JSONResponse(content = movie[0])
    else:
        return JSONResponse(status_code = 404, content = [])
    
# get /movies => query route, the params have a condition with Query
@app.get('/movies/', tags = ['movies'], response_model = List[Movie])
def getMoviesByCategory(category: str = Query(min_length = 5, max_length = 15), year: str = Query(min_length = 4)) -> List[Movie]:
    # filter movies by category or year
    result = list(filter(lambda item: category in item['category'] or year in item['year'], movies))
    if result:
        return JSONResponse(content = result)
    else:
        return JSONResponse(status_code = 404, content = [])
    
# post /movies => to create a new movie
@app.post('/movies', tags = ['movies'], response_model = dict, status_code = 201)
def createMovie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code = 201, content = {
        "message": "Movie saved succesfully"
    })

# put /movies => to update a movie
@app.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def updateMovie(id: int, movie: Movie) -> dict:
    # loop movies
    for item in movies:
        # if movie was fund by id
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            break

    return JSONResponse(status_code = 200, content = {
        "message": "Movie udpated succesfully"
    })

# delete /movies => to delete a movie
@app.delete('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def deleteMovie(id: int) -> dict:
    # loop movies
    for movie in movies:
        # if movie was fund by id
        if movie['id'] == id:
            movies.remove(movie)
            break

    return JSONResponse(status_code = 200, content = {
        "message": "Movie deleted succesfully"
    })