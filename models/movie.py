from config.database import Base
from sqlalchemy import Column, Integer, String, Float

# Class Movie
class Movie(Base):

    # define table name
    __tablename__ = "movies"

    # define columns
    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)