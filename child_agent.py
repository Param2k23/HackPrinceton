from base_agent import BaseAgent, LLMInterface, DatabaseInterface
from typing import Optional, Dict, Any

class SimpleChildAgent(BaseAgent):
    """A simpler implementation of ChildAgent for persona-based interactions"""
    def __init__(self, user_data: Dict[str, Any]):
        self.name = user_data["name"]
        self.age = user_data["age"]
        self.occupation = user_data["occupation"]
        self.relationships = user_data["relationships"]
        self.likings = user_data["likings"]
        self.dislikings = user_data["dislikings"]
        
    def process_prompt(self, prompt: str) -> str:
        """Process the prompt with child-like characteristics"""
        response = f"As {self.name}, a {self.age} year old {self.occupation}, "
        
        # Add child-like enthusiasm for likes
        for like in self.likings:
            if like.lower() in prompt.lower():
                response += f"I really really love {like}! "
        
        # Add child-like aversion for dislikes
        for dislike in self.dislikings:
            if dislike.lower() in prompt.lower():
                response += f"Eww, I hate {dislike}! "
        
        # Add relationship context if mentioned
        for person, relation in self.relationships.items():
            if person.lower() in prompt.lower():
                response += f"{person} is my {relation} and "
        
        # Add age-appropriate response style
        if len(response.split()) < 10:
            response += "I think this is " + ("cool! " if any(like in prompt.lower() for like in self.likings) 
                                            else "boring! " if any(dislike in prompt.lower() for dislike in self.dislikings)
                                            else "interesting, I guess. ")
        
        return response.strip()

# Keep the original ChildAgent class for compatibility
class ChildAgent(BaseAgent):
    """The original ChildAgent implementation"""
    def __init__(
        self,
        name: str,
        llm: LLMInterface,
        db: Optional[DatabaseInterface] = None,
        child_info: Dict[str, Any] = None
    ):
        super().__init__(name, llm, db)
        self.child_info = child_info or {}

    async def initialize(self) -> None:
        """Initialize the agent"""
        pass

    async def process(self, input_data: Any) -> Any:
        """Process input data"""
        pass
