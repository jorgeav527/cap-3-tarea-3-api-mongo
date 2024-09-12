from fastapi import FastAPI
#IMPORTAR LA RUTA A USAR
from routes.Post import post_router

app = FastAPI()

app.include_router(post_router)

# # Start the server
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
