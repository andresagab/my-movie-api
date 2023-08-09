from pydantic import Field, BaseModel
from typing import Optional

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