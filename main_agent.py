import json
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from jose import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt
from parent_agent import SimpleParentAgent
from child_agent import SimpleChildAgent
from base_agent import BaseAgent
from grok_llm import GrokLLM
from json_db import JsonDatabaseInterface

# Load environment variables from .env file
load_dotenv()

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class User(BaseModel):
    username: str
    email: str
    password: str
    role: str

class MainAgent:
    def __init__(self):
        self.db_interface = JsonDatabaseInterface()
        self.grok_llm = GrokLLM(
            api_key=os.getenv("GROK_API_KEY"),
            api_base=os.getenv("GROK_API_BASE")
        )
        self.current_user = None
        self.jwt_secret = os.getenv("JWT_SECRET", "your-secret-key")

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data if successful"""
        try:
            # Query database for user by email
            user_data = await self.db_interface.fetch_context({"email": email})
            if not user_data:
                return None
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                return None
            
            return user_data
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None

    def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT token for authenticated user"""
        token_data = {
            "sub": user_data["username"],
            "email": user_data["email"],
            "role": user_data["role"]
        }
        return jwt.encode(token_data, self.jwt_secret, algorithm="HS256")

    async def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information from database"""
        return await self.db_interface.fetch_context({"username": username})

    async def get_related_person_info(self, username: str, relation_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a related person"""
        return await self.db_interface.fetch_context({
            "relation_query": {
                "username": username,
                "relation_name": relation_name
            }
        })

    def create_agent_for_relationship(self, user_data: Dict[str, Any], relation_type: str) -> BaseAgent:
        """Create appropriate agent based on relationship type"""
        name = user_data.get("name", "Unknown")
        if "father" in relation_type or "mother" in relation_type or "grandfather" in relation_type:
            return SimpleParentAgent(name, self.grok_llm, self.db_interface, user_data)
        elif "son" in relation_type or "daughter" in relation_type or "child" in relation_type:
            return SimpleChildAgent(name, self.grok_llm, self.db_interface, user_data)
        else:
            return BaseAgent(name, self.grok_llm, self.db_interface, user_data)

    async def handle_conversation(self, username: str, prompt: str) -> str:
        """Handle conversation with appropriate agent"""
        self.current_user = await self.get_user_info(username)
        if not self.current_user:
            return "User not found in database!"

        # Check if the prompt mentions any relationships
        for person, relationship in self.current_user["relationships"].items():
            if person.lower() in prompt.lower():
                related_person = await self.get_related_person_info(username, person)
                if related_person:
                    agent = self.create_agent_for_relationship(related_person, relationship)
                    return await agent.process_prompt(prompt)

        # If no relationships mentioned, use base agent
        agent = BaseAgent(self.current_user["name"], self.grok_llm, self.db_interface, self.current_user)
        return await agent.process_prompt(prompt)

# Create main agent instance
main_agent = MainAgent()

@app.post("/auth/login")
async def login(request: LoginRequest):
    user = await main_agent.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = main_agent.create_access_token(user)
    return {
        "token": access_token,
        "role": user["role"],
        "username": user["username"]
    }

@app.get("/user/{username}")
async def get_user(username: str):
    user = await main_agent.get_user_info(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/conversation/{username}")
async def conversation(username: str, prompt: str):
    response = await main_agent.handle_conversation(username, prompt)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
