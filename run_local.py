# run_local.py
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from typing import cast
from langchain_core.messages import convert_to_messages
from langgraph.graph import MessagesState
import pprint

# Import the supervisor graph creator instead of the single agent
from agent.accounting_agent import AccountingAgent
import os

# load_dotenv()
load_dotenv(override=True)


def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)


def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print("\n")


def main():
    print("Local Accounting Agent running. Type 'exit' to quit.")
    # Initialize AccountingAgent with environment settings
    project_id = os.getenv("GCLOUD_PROJECT")
    location = os.getenv("GCLOUD_REGION")
    model_name = os.getenv("OPENAI_MODEL")
    staging_bucket = os.getenv("GCS_BUCKET")
    supabase_url = os.getenv("SUPABASE_URL", "https://your-supabase-url.supabase.co")
    supabase_key = os.getenv("SUPABASE_KEY", "your-supabase-key")
    staging_bucket = cast(str, staging_bucket)

    print(f"Project: {project_id}, Location: {location}, Model: {model_name}")

    if not all([project_id, location, model_name]):
        raise ValueError(
            "GCLOUD_PROJECT, GCLOUD_REGION, and OPENAI_MODEL must be set in .env file"
        )
    # Type narrowing after validation
    assert project_id is not None and location is not None and model_name is not None
    agent = AccountingAgent(
        model=model_name,
        tools=[],  # Add any local tool functions if needed
        project=project_id,
        location=location,
        bucket=staging_bucket,
    )
    agent.set_up()

    # app = agent.graph

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        initial_state = MessagesState(messages=[HumanMessage(content=user_input)])

        # Stream the full multi-agent process
        # for chunk in app.stream(initial_state, {"recursion_limit": 10}):
        #     pretty_print_messages(chunk, last_message=True)

        for chunk in agent.stream_query(input=initial_state):

            pprint.pprint(chunk, depth=3)


if __name__ == "__main__":
    main()
