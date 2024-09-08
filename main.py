from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["fastapi"]
posts_collection = db["post"]

# Models
class Post(BaseModel):
    id: Optional[str]
    title: str
    content: str
    created: datetime = None

class PostCreate(BaseModel):
    title: str
    content: str

# Route for home page (index)
@app.get("/")
async def index():
    return JSONResponse(content={"message": "Welcome to the API"})

# Route to get all posts
@app.get("/post", response_model=List[Post])
async def get_all_post():
    posts = posts_collection.find()
    return [
        Post(
            id=str(post["_id"]),
            title=post["title"],
            content=post["content"],
            created=post.get("created")
        )
        for post in posts
    ]

# Route to get a single post by ID
@app.get("/post/{post_id}", response_model=Post)
async def get_one_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(
        id=str(post["_id"]),
        title=post["title"],
        content=post["content"],
        created=post.get("created")
    )

# Route to create a new post using request body
@app.post("/post/create", response_model=Post)
async def create_one_post(post: PostCreate):
    if not post.title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    created_time = datetime.now()
    new_post = {"title": post.title, "content": post.content, "created": created_time}
    result = posts_collection.insert_one(new_post)
    
    created_post = posts_collection.find_one({"_id": result.inserted_id})
    return Post(
        id=str(created_post["_id"]),
        title=created_post["title"],
        content=created_post["content"],
        created=created_post["created"]
    )

# Route to edit a post by ID
@app.put("/post/edit/{post_id}", response_model=Post)
async def edit_one_post(post_id: str, post: PostCreate):
    existing_post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if not post.title:
        raise HTTPException(status_code=400, detail="Title is required")

    updated_post = {"title": post.title, "content": post.content}
    posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": updated_post})
    
    updated_post = posts_collection.find_one({"_id": ObjectId(post_id)})
    return Post(
        id=str(updated_post["_id"]),
        title=updated_post["title"],
        content=updated_post["content"],
        created=updated_post.get("created")
    )

# Route to delete a post by ID
@app.delete("/post/delete/{post_id}", response_model=dict)
async def delete_one_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    posts_collection.delete_one({"_id": ObjectId(post_id)})
    return {"message": "Post deleted successfully"}

# # Start the server
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
