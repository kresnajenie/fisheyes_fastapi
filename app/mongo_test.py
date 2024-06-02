import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB client
mongo_url = os.getenv("MONGO_URL", "mongodb://rootuser:rootpass@localhost:27017/")
# mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
# mongo_url = os.getenv("MONGO_URL", "mongodb://cmm200-136.ucsd.edu:27017/")
mongo_client = MongoClient(mongo_url)

# Function to save data to MongoDB with dynamic database and collection selection
def save_to_mongodb(collection_name, _id, values, db_name="genedata"):
    db = mongo_client[db_name]
    collection = db[collection_name]
    collection.insert_one({
        "_id": _id,
        "values": values
    })

# Function to retrieve data from MongoDB with dynamic database and collection selection
def retrieve_from_mongodb(collection_name, document_id, db_name="genedata"):
    db = mongo_client[db_name]
    collection = db[collection_name]
    print(collection.find_one({"_id": document_id}))
    return collection.find_one({"_id": document_id})

# if __name__ == "__main__":
#     # Example usage
#     document_to_save = {"_id": "example_id", "content": "hello"}
#     save_to_mongodb("test_db", "test_collection", document_to_save)
#     retrieved_document = retrieve_from_mongodb("test_db", "test_collection", "example_id")
#     print(retrieved_document)
