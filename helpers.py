import datetime
from db import collection  # import collection from db.py

async def save_result(file_name: str, query: str, result: str):
    """Save analysis result to MongoDB"""
    data = {
        "file_name": file_name,
        "query": query,
        "result": result,
        "timestamp": datetime.datetime.utcnow()
    }
    await collection.insert_one(data)
