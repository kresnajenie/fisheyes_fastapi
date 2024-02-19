from fastapi import FastAPI, HTTPException
import redis_test as re
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Define a list of origins that should be allowed to make requests
# You can use ["*"] to allow all origins
origins = [
    "https://fishies.techkyra.com",
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
class RedisData(BaseModel):
    key: str
    value: str


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

@app.get("/getdata")
async def fetch_data(col: str):
# async def fetch_json():
    return {"data": re.retrieve_from_redis(col)}

@app.post("/savedata")
async def save_data(data: RedisData):
    # Use the function from your redis_test module to save data to Redis
    try:
        re.save_to_redis(data.key, data.value)
        return {"message": f"Data saved to Redis under key: {data.key}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
