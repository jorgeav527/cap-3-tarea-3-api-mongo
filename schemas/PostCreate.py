from pydantic import BaseModel, Field

class PostCreate(BaseModel):
    title: str = Field(min_length=5, max_length=25)
    content: str = Field(min_length=14, max_length=150)