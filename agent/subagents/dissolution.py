from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from ..tools.dissolution_tools import dissolution_tool_list


def create_dissolution_agent():
    """Creates the company dissolution agent."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    return create_react_agent(llm, dissolution_tool_list, name="dissolution_agent")
