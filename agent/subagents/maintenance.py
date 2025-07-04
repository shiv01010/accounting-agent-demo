from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from ..tools.maintenance_tools import maintenance_tool_list


def create_maintenance_agent():
    """Creates the company maintenance agent."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    return create_react_agent(llm, maintenance_tool_list, name="maintenance_agent")
