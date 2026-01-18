from pydantic import BaseModel

class TextIn(BaseModel):
    text: str

class CategoryResponse(BaseModel):
    category: str
    reply: str
