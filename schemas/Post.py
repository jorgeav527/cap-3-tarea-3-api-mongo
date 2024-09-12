from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Models
class Post(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    created: datetime = None

#METODO PARA SIMPLIFICAR CLASE POST
def post_dict(post):
    return Post(
        id=str(post["_id"]),
        title=post["title"],
        content=post["content"],
        created=post.get("created")
    )