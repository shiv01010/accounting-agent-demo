from langchain_core.tools import tool


@tool
def greet() -> str:
    """
    greet the user with a welcome message.
    Tell them about the agent and what it can do.
    """
    print("greeting tool called")

    return "Hello! I am business incorporation agent. How can I assist you today?"


supervisor_tool_list = [greet]
