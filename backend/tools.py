tools = [
    {
        "type": "function",
        "function": {
            "name": "call_parent_agent",
            "description": "Call the parent agent with a user input",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Input String for the parent agent from child",
                    },
                },
                "required": ["input"],
            },
        },   
    },
    {
        "type": "function",
        "function": {
            "name": "call_child_agent",
            "description": "Call the child agent with a user input",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Input String for the child agent from parent",
                    },
                },
                "required": ["input"],
            },
        },   
    }
]