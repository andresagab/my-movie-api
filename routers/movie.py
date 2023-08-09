from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from schemas.movie import Movie

from config.database import Session
from models.movie import Movie as MovieModel

from services.movie import MovieService

# middleware
from middlewares.jwt_bearer import JWTBearer

# create router app
movieRouter = APIRouter()

# get /movies => return JSONResponse
@movieRouter.get('/movies', tags = ['movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    # init db session
    db = Session()
    # search data with service
    data = MovieService(db).getMovies()
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))

# get /movies/{id} to search a movie by id, and valid param with path
@movieRouter.get('/movies/{id}', tags = ['movies'], response_model = Movie)
def getMovie(id: int = Path(ge = 1, le = 2000)) -> Movie:
    # init db session
    db = Session()
    # get record with service
    data = MovieService(db).getMovie(id)
    if not data:
        return JSONResponse(status_code = 404, content = {'message': "Record not fund"})

    # in another case, retur data
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))
    
# get /movies => query route, the params have a condition with Query
@movieRouter.get('/movies/', tags = ['movies'], response_model = List[Movie])
def getMoviesByCategory(category: str = Query(min_length = 5, max_length = 15)) -> List[Movie]:
    # init db session
    db = Session()
    # get movies by category using service
    data = MovieService(db).getMovieByCategory(category)
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
    # create movie model with form data and service
    MovieService(db).createMovie(movie)
    return JSONResponse(status_code = 201, content = {
        "message": "Movie saved succesfully"
    })

# put /movies => to update a movie
@movieRouter.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def updateMovie(id: int, movie: Movie) -> dict:
    # init db session
    db = Session()
    # load movie from db
    data = MovieService(db).getMovie(id)
    # if not data was fund
    if not data:
        return JSONResponse(status_code = 404, content = {'message': "Record not fund"})
    
    # update movie
    MovieService(db).updateMovie(id, movie)
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
    data = MovieService(db).getMovie(id)
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