import redis
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Redis connection once, it will be switched to the correct db in the functions
# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')  # Default to db 0
# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')  # Default to db 0
redis_url = os.getenv("REDIS_URL")
redis_client = redis.StrictRedis.from_url(redis_url)

# Function to save data to Redis with database selection
def save_to_redis(key, value, db=0):
    # Switch to the specified database
    redis_client.connection_pool.connection_kwargs['db'] = db
    redis_client.set(key, value)

# Function to retrieve data from Redis with database selection
def retrieve_from_redis(key, db=0):
    # Switch to the specified database
    redis_client.connection_pool.connection_kwargs['db'] = db
    return redis_client.get(key)

if __name__ == "__main__":
    # Example usage
    save_to_redis("test", "hello", 1)
    print(retrieve_from_redis("test", 1))
