from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request
from jwt_manager import create_token, valid_token
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder

from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

# APP

# create app
app = FastAPI()
# set title of app
app.title = "My app with FastAPI"
# set version
app.version = "0.0.1"

Base.metadata.create_all(bind = engine)

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
    # init db session
    db = Session()
    # search data
    data = db.query(MovieModel).all()
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))

# get /movies/{id} to search a movie by id, and valid param with path
@app.get('/movies/{id}', tags = ['movies'], response_model = Movie)
def getMovie(id: int = Path(ge = 1, le = 2000)) -> Movie:
    # init db session
    db = Session()
    # filter by id and get first result
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(status_code = 404, content = {'message': "Record not fund"})

    # in another case, retur data
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))
    
# get /movies => query route, the params have a condition with Query
@app.get('/movies/', tags = ['movies'], response_model = List[Movie])
def getMoviesByCategory(category: str = Query(min_length = 5, max_length = 15), year: str = Query(min_length = 4)) -> List[Movie]:
    # init db session
    db = Session()
    # filter data by category or year
    data = db.query(MovieModel).filter(category.lower() in str(MovieModel.category).lower() or MovieModel.year == year).all()
    # if data, then return data, else return empty list
    if data:
        return JSONResponse(status_code = 200, content = jsonable_encoder(data))
    else:
        return JSONResponse(status_code = 404, content = [])
    
# post /movies => to create a new movie
@app.post('/movies', tags = ['movies'], response_model = dict, status_code = 201)
def createMovie(movie: Movie) -> dict:
    # init db session
    db = Session()
    # create movie model with form data
    new_movie = MovieModel(**movie.dict())
    # save on database
    db.add(new_movie)
    # commit changes
    db.commit()
    # save on memory
    movies.append(movie)
    return JSONResponse(status_code = 201, content = {
        "message": "Movie saved succesfully"
    })

# put /movies => to update a movie
@app.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def updateMovie(id: int, movie: Movie) -> dict:
    # init db session
    db = Session()
    # load record
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    # if not data was fund
    if not data:
        return JSONResponse(status_code = 404, content = {'message': "Record not fund"})
    
    # set attributes
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    # commit changes
    db.commit()
    
    return JSONResponse(status_code = 200, content = {
        "message": "Movie udpated succesfully"
    })

# delete /movies => to delete a movie
@app.delete('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def deleteMovie(id: int) -> dict:
    # init db session
    db = Session()

    # search record
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    # if record was not fund
    if not data:
        return JSONResponse(status_code = 404, content = {'message': "Record not fund"})
    
    # remove record
    db.delete(data)
    # commit changes
    db.commit()

    return JSONResponse(status_code = 200, content = {
        "message": "Movie deleted succesfully"
    })