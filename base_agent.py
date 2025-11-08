from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, AsyncIterator
from dataclasses import dataclass

@dataclass
class PromptTemplate:
    """Class to manage prompt templates for agents"""
    name: str
    template: str
    variables: List[str]

    def format(self, **kwargs) -> str:
        """Format the prompt template with given variables"""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable {e} in prompt template {self.name}")

class Context:
    """Class to manage context information for agents"""
    def __init__(self):
        self._context: Dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        """Add or update context information"""
        self._context[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve context information"""
        return self._context.get(key, default)

    def clear(self) -> None:
        """Clear all context information"""
        self._context.clear()

class LLMInterface(ABC):
    """Abstract base class for LLM interactions"""
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM"""
        pass

    @abstractmethod
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream response from LLM"""
        pass

class DatabaseInterface(ABC):
    """Abstract base class for database interactions"""
    @abstractmethod
    async def fetch_context(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch context from database"""
        pass

    @abstractmethod
    async def save_context(self, context: Dict[str, Any]) -> None:
        """Save context to database"""
        pass

class BaseAgent(ABC):
    """Base agent class that can be extended by specific agents"""
    def __init__(
        self,
        name: str,
        llm: LLMInterface,
        db: Optional[DatabaseInterface] = None,
        user_data: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.llm = llm
        self.db = db
        self.context = Context()
        self.prompts: Dict[str, PromptTemplate] = {}
        
        # Initialize with user data if provided
        if user_data:
            self.name = user_data.get("name", name)
            self.age = user_data.get("age")
            self.occupation = user_data.get("occupation")
            self.relationships = user_data.get("relationships", {})
            self.likings = user_data.get("likings", [])
            self.dislikings = user_data.get("dislikings", [])

    def add_prompt(self, prompt: PromptTemplate) -> None:
        """Add a prompt template to the agent"""
        self.prompts[prompt.name] = prompt

    def get_prompt(self, name: str, **kwargs) -> str:
        """Get a formatted prompt by name"""
        if name not in self.prompts:
            raise ValueError(f"Prompt template '{name}' not found")
        return self.prompts[name].format(**kwargs)

    async def load_context(self, query: Dict[str, Any]) -> None:
        """Load context from database"""
        if self.db is None:
            raise ValueError("No database interface configured")
        context_data = await self.db.fetch_context(query)
        for key, value in context_data.items():
            self.context.add(key, value)

    async def save_context(self) -> None:
        """Save current context to database"""
        if self.db is None:
            raise ValueError("No database interface configured")
        await self.db.save_context(self.context._context)

    async def process(self, input_data: Any) -> Any:
        """Process input data and return response"""
        if isinstance(input_data, str):
            return await self.process_prompt(input_data)
        elif isinstance(input_data, dict):
            return await self.process_structured_input(input_data)
        raise ValueError("Input must be either a string prompt or a structured dictionary")

    async def process_prompt(self, prompt: str) -> str:
        """Process a text prompt using the agent's characteristics"""
        # Build context-aware prompt
        context_prompt = self._build_context_prompt(prompt)
        
        # Generate response using Grok LLM
        try:
            response = await self.llm.generate(context_prompt)
            return self._post_process_response(response)
        except Exception as e:
            raise AgentException(f"Failed to generate response: {str(e)}")

    async def process_structured_input(self, input_data: Dict[str, Any]) -> Any:
        """Process structured input data"""
        # Handle different types of structured inputs
        input_type = input_data.get("type", "general")
        content = input_data.get("content", "")
        
        if input_type in self.prompts:
            prompt = self.get_prompt(input_type, **input_data)
        else:
            prompt = self._build_context_prompt(content)
        
        return await self.llm.generate(prompt)

    def _build_context_prompt(self, user_input: str) -> str:
        """Build a context-aware prompt incorporating agent's characteristics"""
        context_parts = [
            f"You are {self.name}",
            f"Age: {self.age}" if hasattr(self, "age") else "",
            f"Occupation: {self.occupation}" if hasattr(self, "occupation") else "",
        ]

        # Add relationships context if relevant
        if hasattr(self, "relationships"):
            for person, relation in self.relationships.items():
                if person.lower() in user_input.lower():
                    context_parts.append(f"You have a relationship with {person} as their {relation}")

        # Add preferences context if relevant
        if hasattr(self, "likings"):
            likes_context = [like for like in self.likings if like.lower() in user_input.lower()]
            if likes_context:
                context_parts.append(f"You particularly enjoy: {', '.join(likes_context)}")

        if hasattr(self, "dislikings"):
            dislikes_context = [dislike for dislike in self.dislikings if dislike.lower() in user_input.lower()]
            if dislikes_context:
                context_parts.append(f"You dislike: {', '.join(dislikes_context)}")

        # Build final prompt
        context = ". ".join(filter(None, context_parts))
        return f"{context}\n\nUser input: {user_input}\n\nRespond in character, considering your personality and background:"

    def _post_process_response(self, response: str) -> str:
        """Post-process the LLM response to ensure it aligns with agent characteristics"""
        return response.strip()

    async def initialize(self) -> None:
        """Initialize agent with necessary setup"""
        if self.db:
            try:
                await self.load_context({"agent_id": self.name})
            except Exception as e:
                raise AgentException(f"Failed to initialize agent: {str(e)}")

class AgentException(Exception):
    """Base exception class for agent-related errors"""
    pass

class PromptException(AgentException):
    """Exception for prompt-related errors"""
    pass

class ContextException(AgentException):
    """Exception for context-related errors"""
    pass
