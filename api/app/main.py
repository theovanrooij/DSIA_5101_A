import datetime
from fastapi import FastAPI

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"Hello": "World API"}

@app.get("/date")
def read_root():
    return {"Date": datetime.datetime.today()}