from typing import Dict, Any
from base_agent import DatabaseInterface
import json
import os

class JsonDatabaseInterface(DatabaseInterface):
    """Implementation of DatabaseInterface using JSON file storage"""
    def __init__(self, db_path: str = "user_database.json"):
        self.db_path = db_path

    async def fetch_context(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch context from JSON database"""
        try:
            if not os.path.exists(self.db_path):
                return {}
            
            with open(self.db_path, 'r') as f:
                data = json.load(f)

            # If email is provided in query for authentication
            if "email" in query:
                for username, user_data in data.get("current_users", {}).items():
                    if user_data.get("email") == query["email"]:
                        return user_data
                return {}
            
            # If username is provided in query, return that user's data
            if "username" in query:
                return data.get("current_users", {}).get(query["username"], {})
            
            # If looking for related person
            if "relation_query" in query:
                username = query["relation_query"].get("username")
                relation_name = query["relation_query"].get("relation_name")
                
                if username and relation_name:
                    user_data = data.get("current_users", {}).get(username, {})
                    relationships = user_data.get("relationships", {})
                    
                    if relation_name in relationships:
                        related_username = relationships[relation_name]
                        return data.get("current_users", {}).get(related_username, {})
            
            return {}
            
        except Exception as e:
            print(f"Error fetching from database: {str(e)}")
            return {}

    async def save_context(self, context: Dict[str, Any]) -> None:
        """Save context to JSON database"""
        try:
            if not os.path.exists(self.db_path):
                data = {"current_users": {}}
            else:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
            
            # Update the database with new context
            if "username" in context:
                username = context.pop("username")
                data["current_users"][username] = context
            
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            print(f"Error saving to database: {str(e)}")
            raise