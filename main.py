from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config.database import engine, Base

# middleware
from middlewares.error_handler import ErrorHandler

# routers
from routers.movie import movieRouter
from routers.user import userRouter

# APP

# create app
app = FastAPI()
# set title of app
app.title = "My app with FastAPI"
# set version
app.version = "0.0.1"

# add middlewares to app
app.add_middleware(ErrorHandler)

# include routers
app.include_router(movieRouter)
app.include_router(userRouter)

Base.metadata.create_all(bind = engine)

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

