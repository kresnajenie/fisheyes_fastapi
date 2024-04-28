from fastapi import FastAPI, HTTPException
# import redis_test as re
import mongo_test as mo
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from get_minio import download
# import parse_h5

app = FastAPI()

# Define a list of origins that should be allowed to make requests
# You can use ["*"] to allow all origins
origins = [
    "https://fishies.techkyra.com",
    "https://edward.techkyra.com",
    "https://basel.techkyra.com",
    "https://kresnajenie.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow credentials (cookies, headers)
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define a Pydantic model for the data we expect (key and value)
class MongoData(BaseModel):
    collection: str
    key: str
    values: str


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

@app.get("/getdata")
async def fetch_data(data: str, gene: str):
# async def fetch_json():
    # print(data, gene)
    return mo.retrieve_from_mongodb(data, gene)

@app.post("/savedata")
async def save_data(data: MongoData):
    # Use the function from your redis_test module to save data to Redis
    try:
        mo.save_to_mongodb(data.collection, data.key, data.values)
        return {"message": f"Data saved to Mongo under key: {data.key}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
