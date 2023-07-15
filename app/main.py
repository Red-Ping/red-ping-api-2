from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/login")
def login(username: str, password: str):
    return {"username": username}

@app.post("/signup")
def signup(username: str, password: str):
    return {"username": username}

#Requesting to ping a user
@app.post("/ping_request")
def post_ping_request():
    return {"status": "healthy"}

#Get the current ping requests
@app.get("/ping_request")
def get_ping_request():
    return {"status": "healthy"}

#Sends a ping to a user
@app.post("/ping_send")
def post_ping_send():
    return {"status": "healthy"}

#Get the current pings
@app.get("/ping_send")
def get_ping_send():
    return {"status": "healthy"}