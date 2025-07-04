from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from ..tools.incorporation_tools import incorporation_tool_list

# Create a handoff tool for transferring to the supervisor agent


def create_incorporation_agent():
    """Creates the company incorporation agent."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    return create_react_agent(
        llm,
        incorporation_tool_list,
        name="incorporation_agent",
        # prompt=(
        #     "You are an incorporation agent in a large accounting firm. Your job is to assist users with company registration tasks. "
        #     "You can answer questions about the incorporation process, required documents, and fees. "
        #     "If the user asks for help with a task that is not related to incorporation, transfer them to the supervisor agent."
        #     "If the user asks for help with a task that is not related to any of the sub-agents, you can answer directly as the incorporation agent."
        #     "If you can answer directly, respond as the incorporation agent."
        #     "For incorporation task you first need to collect the required information from the user, such as company name, type of business, and other relevant details. "
        # ),
    )
