from typing import Dict, Any, Optional, List
from datetime import datetime
from base_agent import BaseAgent, LLMInterface, DatabaseInterface, PromptTemplate, Context

class SimpleParentAgent(BaseAgent):
    """A simpler implementation of ParentAgent for persona-based interactions"""
    def __init__(self, user_data: Dict[str, Any]):
        self.name = user_data["name"]
        self.age = user_data["age"]
        self.occupation = user_data["occupation"]
        self.relationships = user_data["relationships"]
        self.likings = user_data["likings"]
        self.dislikings = user_data["dislikings"]

    def process_prompt(self, prompt: str) -> str:
        """Process the prompt with parent-like characteristics"""
        response = f"As {self.name}, a {self.age} year old {self.occupation}, "

        # Add wisdom-based context
        response += "drawing from my experience, "

        # Add parental perspective for likes/dislikes
        for like in self.likings:
            if like.lower() in prompt.lower():
                response += f"I believe {like} is valuable because it enriches our lives. "

        for dislike in self.dislikings:
            if dislike.lower() in prompt.lower():
                response += f"I have concerns about {dislike} because it might not be beneficial. "

        # Add relationship context if mentioned
        for person, relation in self.relationships.items():
            if person.lower() in prompt.lower():
                response += f"As {person}'s {relation}, I feel "

        # Add parental advice style
        if len(response.split()) < 10:
            response += ("I would advise careful consideration of this matter, "
                      "keeping in mind the importance of wisdom and experience. ")

        return response.strip()

class ParentAgent(BaseAgent):
    """Agent that acts as a caring parent figure"""
    
    def __init__(
        self,
        name: str,
        llm: LLMInterface,
        db: Optional[DatabaseInterface] = None,
        parent_info: Dict[str, Any] = None
    ):
        super().__init__(name, llm, db)
        self.parent_info = parent_info or self._get_default_parent_info()
        self._initialize_prompts()

    def _get_default_parent_info(self) -> Dict[str, Any]:
        """Provide default parent information (dummy data)"""
        return {
            "name": "Alex",
            "occupation": "Software Engineer",
            "working_hours": "9 AM - 6 PM",
            "personality_traits": [
                "caring",
                "patient",
                "understanding",
                "supportive"
            ],
            "communication_style": "warm and encouraging",
            "interests": [
                "technology",
                "reading",
                "cooking",
                "outdoor activities"
            ],
            "values": [
                "education",
                "kindness",
                "responsibility",
                "creativity"
            ],
            "child_info": {
                "name": "Sam",
                "age": 12,
                "interests": [
                    "video games",
                    "drawing",
                    "science"
                ],
                "personality": "curious and creative"
            }
        }

    def _initialize_prompts(self) -> None:
        """Initialize prompt templates for different interaction scenarios"""
        self.add_prompt(PromptTemplate(
            name="greeting",
            template=(
                "You are {parent_name}, a caring parent who is currently busy with work "
                "but wants to maintain a warm connection with your child {child_name}. "
                "Despite your physical absence, you want to ensure your child feels loved "
                "and supported. Respond to their greeting in a warm, caring manner while "
                "acknowledging your current situation: {current_situation}"
            ),
            variables=["parent_name", "child_name", "current_situation"]
        ))

        self.add_prompt(PromptTemplate(
            name="daily_support",
            template=(
                "As {parent_name}, provide guidance and support to {child_name} regarding "
                "their current activity or concern: {current_topic}. Remember to be "
                "encouraging and understanding while maintaining your role as a caring "
                "parent who, although busy, always makes time for their child's needs."
            ),
            variables=["parent_name", "child_name", "current_topic"]
        ))

        self.add_prompt(PromptTemplate(
            name="emotional_support",
            template=(
                "Your child {child_name} is experiencing {emotion} about {situation}. "
                "As their parent {parent_name}, provide emotional support and guidance "
                "while acknowledging your current limitations but emphasizing your "
                "unconditional love and support."
            ),
            variables=["parent_name", "child_name", "emotion", "situation"]
        ))

    async def initialize(self) -> None:
        """Initialize agent with necessary setup"""
        if self.db:
            # Load context from database when available
            await self.load_context({"agent_id": self.name})
        else:
            # Use default context
            self.context.add("parent_info", self.parent_info)
            self.context.add("last_interaction", None)
            self.context.add("interaction_history", [])

    def _update_interaction_history(self, interaction: Dict[str, Any]) -> None:
        """Update the interaction history"""
        history = self.context.get("interaction_history", [])
        history.append({
            **interaction,
            "timestamp": datetime.now().isoformat()
        })
        self.context.add("interaction_history", history)
        self.context.add("last_interaction", interaction)

    async def process(self, input_data: Dict[str, Any]) -> str:
        """Process input and generate appropriate parental response"""
        interaction_type = input_data.get("type", "daily_support")
        child_input = input_data.get("content", "")
        
        # Get parent and child info from context
        parent_info = self.context.get("parent_info", self.parent_info)
        child_info = parent_info["child_info"]

        # Prepare prompt based on interaction type
        if interaction_type == "greeting":
            current_time = datetime.now().strftime("%I:%M %p")
            prompt = self.get_prompt(
                "greeting",
                parent_name=parent_info["name"],
                child_name=child_info["name"],
                current_situation=f"Working from home at {current_time}"
            )
        elif interaction_type == "emotional_support":
            prompt = self.get_prompt(
                "emotional_support",
                parent_name=parent_info["name"],
                child_name=child_info["name"],
                emotion=input_data.get("emotion", "concerned"),
                situation=child_input
            )
        else:  # daily_support
            prompt = self.get_prompt(
                "daily_support",
                parent_name=parent_info["name"],
                child_name=child_info["name"],
                current_topic=child_input
            )

        # Generate response using LLM
        response = await self.llm.generate(prompt)

        # Update interaction history
        self._update_interaction_history({
            "type": interaction_type,
            "input": child_input,
            "response": response
        })

        # Save context if database is available
        if self.db:
            await self.save_context()

        return response

    async def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Retrieve conversation history"""
        return self.context.get("interaction_history", [])