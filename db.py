from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")

# Database and collection
db = client["financial_app"]
collection = db["results"]
