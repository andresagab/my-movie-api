from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():

    def __init__(self, db) -> None:
        # init db service
        self.db = db

    '''
    Get all records
    '''
    def getMovies(self):
        # get data from db
        result = self.db.query(MovieModel).all()
        return result
    
    '''
    Get a one movie, filtered by id
    '''
    def getMovie(self, id):
        # filter record by id and get first result
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    '''
    Get movies filtered by category
    '''
    def getMovieByCategory(self, category: str):
        # filter records by category of model
        result = self.db.query(MovieModel).filter(category.lower() in str(MovieModel.category).lower()).all()
        return result
    
    '''
    Create a new movie resource
    '''
    def createMovie(self, movie: Movie):
        # define new movie model with request data
        newMovie = MovieModel(**movie.dict())
        # store in db
        self.db.add(newMovie)
        # commit changes
        self.db.commit()
        return
    
    '''
    Update a movie resource
    '''
    def updateMovie(self, id: int, data: Movie):
        # load movie from db
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        # set movie data
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        # save changes
        self.db.commit()
        return
    
    '''
    Delete a movie resource
    '''
    def deleteMovie(self, movie: Movie):
        # delete movie
        self.db.delete(movie)
        # commit changes
        self.db.commit()
        return
