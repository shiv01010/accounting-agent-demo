from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from ..tools.updation_tools import updation_tool_list


def create_updation_agent():
    """Creates the company maintenance agent."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    return create_react_agent(llm, updation_tool_list, name="updation_agent")
