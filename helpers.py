# helpers.py

import datetime
from db import collection
from fastapi import HTTPException

# -------------------------
# Save analysis result to MongoDB
# -------------------------
async def save_result(file_name: str, query: str, result: str):
    """
    Save the processed financial document result to MongoDB.

    Args:
        file_name (str): Name of the uploaded PDF file
        query (str): User query or instruction
        result (str): Combined analysis result from CrewAI agents
    """
    try:
        data = {
            "file_name": file_name,
            "query": query,
            "result": result,
            "timestamp": datetime.datetime.utcnow()
        }
        await collection.insert_one(data)
    except Exception as e:
        # Raise HTTPException to propagate error in FastAPI
        raise HTTPException(status_code=500, detail=f"Failed to save result: {str(e)}")
