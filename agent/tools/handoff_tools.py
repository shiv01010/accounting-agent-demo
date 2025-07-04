from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.types import Command


def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Transfer to {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            goto=agent_name,
            update={"messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,
        )

    return handoff_tool


# Handoffs

assign_to_incorporation_agent = create_handoff_tool(
    agent_name="incorporation_agent",
    description="Transfer to the incorporation agent for company registration tasks.",
)

assign_to_maintenance_agent = create_handoff_tool(
    agent_name="maintenance_agent",
    description="Transfer to the maintenance agent for company maintenance tasks.",
)

assign_to_dissolution_agent = create_handoff_tool(
    agent_name="dissolution_agent",
    description="Transfer to the dissolution agent for company dissolution tasks.",
)

assign_to_updation_agent = create_handoff_tool(
    agent_name="updation_agent",
    description="Transfer to the updation agent for company updation tasks.",
)
