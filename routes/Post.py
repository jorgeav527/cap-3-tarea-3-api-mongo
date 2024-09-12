from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from typing import List
from datetime import datetime
#IMPORTAR BASE DE DATOS
from config.database import posts_collection
#IMPORTAR LOS SCHEMAS
from schemas.Post import Post, post_dict
from schemas.PostCreate import PostCreate

post_router = APIRouter()

# Route for home page (index)
@post_router.get("/")
async def index():
    return JSONResponse(content={"message": "Welcome to the API"})

# Route to get all posts
@post_router.get("/post", response_model=List[Post], tags=['Posts'], status_code=200)
async def get_all_post():
    posts = posts_collection.find()
    return [post_dict(post) for post in posts]

# Route to get a single post by ID
@post_router.get("/post/{post_id}", response_model=Post, tags=['Posts'], status_code=200)
async def get_one_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return (post_dict(post))

# Route to create a new post using request body
@post_router.post("/post/create", response_model=Post, tags=['Posts'], status_code=201)
async def create_one_post(post: PostCreate):
    if not post.title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    created_time = datetime.now()
    new_post = {"title": post.title, "content": post.content, "created": created_time}
    result = posts_collection.insert_one(new_post)
    
    created_post = posts_collection.find_one({"_id": result.inserted_id})
    return post_dict(created_post)

# Route to edit a post by ID
@post_router.put("/post/edit/{post_id}", response_model=Post, tags=['Posts'], status_code=200)
async def edit_one_post(post_id: str, post: PostCreate):
    existing_post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if not post.title:
        raise HTTPException(status_code=400, detail="Title is required")

    updated_post = {"title": post.title, "content": post.content}
    posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": updated_post})
    
    updated_post = posts_collection.find_one({"_id": ObjectId(post_id)})
    return post_dict(updated_post)

# Route to delete a post by ID
@post_router.delete("/post/delete/{post_id}", response_model=dict, tags=['Posts'], status_code=200)
async def delete_one_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    posts_collection.delete_one({"_id": ObjectId(post_id)})
    return {"message": "Post deleted successfully"}