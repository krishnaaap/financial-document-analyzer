import asyncio
import datetime
from db import collection

async def test_save():
    data = {
        "file_name": "sample.pdf",
        "query": "Test query",
        "result": "This is a test result",
        "timestamp": datetime.datetime.utcnow()
    }
    await collection.insert_one(data)
    print("Saved to MongoDB!")

asyncio.run(test_save())
