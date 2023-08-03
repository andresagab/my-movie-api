from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional

from config.database import Session
from models.movie import Movie as MovieModel

# middleware
from middlewares.jwt_bearer import JWTBearer

# create router app
movieRouter = APIRouter()

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

# get /movies => return JSONResponse
@movieRouter.get('/movies', tags = ['movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    # init db session
    db = Session()
    # search data
    data = db.query(MovieModel).all()
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))

# get /movies/{id} to search a movie by id, and valid param with path
@movieRouter.get('/movies/{id}', tags = ['movies'], response_model = Movie)
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
@movieRouter.get('/movies/', tags = ['movies'], response_model = List[Movie])
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
@movieRouter.post('/movies', tags = ['movies'], response_model = dict, status_code = 201)
def createMovie(movie: Movie) -> dict:
    # init db session
    db = Session()
    # create movie model with form data
    new_movie = MovieModel(**movie.dict())
    # save on database
    db.add(new_movie)
    # commit changes
    db.commit()
    return JSONResponse(status_code = 201, content = {
        "message": "Movie saved succesfully"
    })

# put /movies => to update a movie
@movieRouter.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
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
@movieRouter.delete('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
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