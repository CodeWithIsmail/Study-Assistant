# MongoDB Database Configuration and User Model
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from typing import Optional, Dict, Any
import asyncio

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

# Global database instance
db = MongoDB()

async def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.getenv("MONGODB_URL", "")
    
    if not mongo_url:
        print("Warning: MONGODB_URL not set in environment variables")
        return None
    
    try:
        db.client = AsyncIOMotorClient(mongo_url)
        db.database = db.client.study_assistant
        
        # Test connection
        await db.client.admin.command('ping')
        print("Successfully connected to MongoDB")
        return db.database
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()

class UserDatabase:
    def __init__(self):
        self.collection_name = "users"
    
    def get_collection(self):
        """Get users collection"""
        if db.database is None:
            raise Exception("Database not connected. Please check MONGODB_URL")
        return db.database[self.collection_name]
    
    async def create_user(self, email: str, hashed_password: str, full_name: str = None) -> str:
        """Create a new user and return user ID"""
        collection = self.get_collection()
        
        # Check if user already exists
        existing_user = await collection.find_one({"email": email})
        if existing_user:
            raise ValueError("Email already exists")
        
        user_doc = {
            "email": email,
            "hashed_password": hashed_password,
            "full_name": full_name,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        
        result = await collection.insert_one(user_doc)
        return str(result.inserted_id)
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[Any, Any]]:
        """Get user by email"""
        collection = self.get_collection()
        user = await collection.find_one({"email": email})
        
        if user:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string
            return user
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[Any, Any]]:
        """Get user by ID"""
        collection = self.get_collection()
        
        try:
            user = await collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])  # Convert ObjectId to string
                return user
        except Exception as e:
            print(f"Error getting user by ID: {e}")
        
        return None
    
    async def update_last_login(self, user_id: str):
        """Update user's last login timestamp"""
        collection = self.get_collection()
        
        try:
            await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow()}}
            )
        except Exception as e:
            print(f"Error updating last login: {e}")
    
    async def deactivate_user(self, user_id: str):
        """Deactivate a user account"""
        collection = self.get_collection()
        
        try:
            await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_active": False}}
            )
        except Exception as e:
            print(f"Error deactivating user: {e}")
    
    async def update_user(self, user_id: str, update_data: Dict[str, Any]):
        """Update user data"""
        collection = self.get_collection()
        
        try:
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list:
        """Get all users with pagination"""
        collection = self.get_collection()
        
        cursor = collection.find({}).skip(skip).limit(limit)
        users = []
        
        async for user in cursor:
            user["_id"] = str(user["_id"])
            # Remove sensitive data
            user.pop("hashed_password", None)
            users.append(user)
        
        return users
    
    async def count_users(self) -> int:
        """Count total number of users"""
        collection = self.get_collection()
        return await collection.count_documents({})

# Global user database instance
user_db = UserDatabase()
