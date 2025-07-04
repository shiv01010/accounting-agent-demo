# agent/supervisor.py

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START, MessagesState

# from .state import AgentStat
from .subagents.incorporation import create_incorporation_agent

# from IPython.display import display, Image
from .subagents.updation import create_updation_agent
from .subagents.maintenance import create_maintenance_agent
from .subagents.dissolution import create_dissolution_agent
from langgraph.prebuilt import create_react_agent
from .tools.handoff_tools import (
    assign_to_dissolution_agent,
    assign_to_incorporation_agent,
    assign_to_maintenance_agent,
    assign_to_updation_agent,
)

supervisor_agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4o-mini"),
    tools=[
        assign_to_incorporation_agent,
        assign_to_updation_agent,
        assign_to_maintenance_agent,
        assign_to_dissolution_agent,
    ],
    name="supervisor_agent",
    prompt=(
        "You are a supervisor_agent in a large accounting firm. Your job is to route user requests to the correct sub-agent "
        "or handle simple conversational responses yourself. Based on the user's request, choose the appropriate agent "
        "from the following options: incorporation, updation, maintenance, dissolution, or END if the task is complete. "
        "If you can answer directly, respond as the supervisor_agent."
    ),
)

incorporation_agent = create_incorporation_agent()
updation_agent = create_updation_agent()
maintenance_agent = create_maintenance_agent()
dissolution_agent = create_dissolution_agent()


# def create_supervisor_graph():
#     workflow = StateGraph(MessagesState)

#     workflow.add_node("supervisor", supervisor_agent)
#     workflow.add_node("incorporation_agent", incorporation_agent)
#     workflow.add_node("updation_agent", updation_agent)
#     workflow.add_node("maintenance_agent", maintenance_agent)
#     workflow.add_node("dissolution_agent", dissolution_agent)

#     # Start flow
#     workflow.set_entry_point("supervisor")

#     # Conditional transition from supervisor to correct agent
#     workflow.add_conditional_edges(
#         "supervisor",
#         lambda state: state,
#         {
#             "incorporation_agent": "incorporation_agent",
#             "updation_agent": "updation_agent",
#             "maintenance_agent": "maintenance_agent",
#             "dissolution_agent": "dissolution_agent",
#             "__end__": END,
#         },
#     )


#     # Compile and visualize
#     graph = workflow.compile()
#     graph.get_graph().draw_png("graph.png")

#     return graph


supervisor_graph = (
    StateGraph(MessagesState)
    .add_node(
        "supervisor_agent",
        supervisor_agent,
        destinations=(
            "incorporation_agent",
            "updation_agent",
            "maintenance_agent",
            "dissolution_agent",
            END,
        ),
    )
    .add_node("incorporation_agent", incorporation_agent)
    .add_node("updation_agent", updation_agent)
    .add_node("maintenance_agent", maintenance_agent)
    .add_node("dissolution_agent", dissolution_agent)
    .add_edge(START, "supervisor_agent")
    .add_edge("incorporation_agent", "supervisor_agent")
    .add_edge("updation_agent", "supervisor_agent")
    .add_edge("maintenance_agent", "supervisor_agent")
    .add_edge("dissolution_agent", "supervisor_agent")
    .compile()
)

# supervisor_graph.get_graph().draw_png("graph.png")
