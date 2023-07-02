import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# set name of data base
sqlite_file_name = "../database.sqlite"
# define base directory with path of current file
base_dir = os.path.dirname(os.path.realpath(__file__))

# define URL of database
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# define engine
engine = create_engine(database_url, echo = True)

# define session
Session = sessionmaker(bind = engine)

# define base to manage database
Base = declarative_base()