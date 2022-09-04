import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.socket.main import app as socket_app
from app.routers import auth, user, listings, chats, files, utils, reviews

from config import ENV

app = FastAPI()


###############################
# Enable CORS
###############################


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


###############################
# Include All Routers
###############################

app.include_router(auth.router)
app.include_router(user.router)

app.include_router(listings.router)
app.include_router(chats.router)
app.include_router(reviews.router)

app.include_router(files.router)
app.include_router(utils.router)


###############################
# Serve Static (Uploaded) Files
###############################

app.mount("/static", StaticFiles(directory="uploads"), name="static")


###############################
# Mount SocketIO App
###############################


app.mount("/ws", socket_app, name="socket")


###############################
# App Status Endpoint
###############################

@app.get("/")
def get_status():
    return {"status": True, "python": sys.version, 'env': ENV}
