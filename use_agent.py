from vertexai import agent_engines
import json


# Define the pretty-printing function here or import it
def pretty_print_agent_step(chunk):
    """
    A robust function to parse and print a streaming chunk from the agent graph
    in a human-readable format. It handles multiple message formats to prevent errors.

    Args:
        chunk (dict): A dictionary representing the state of an agent at a single step.
    """
    # The chunk is a dictionary where the key is the active agent's name
    for agent_name, state in chunk.items():
        messages = state.get("messages", [])
        if not messages:
            continue

        latest_message = messages[-1]

        print(f"🕵️  **Active Agent:** {agent_name.replace('_', ' ').title()}")

        # Check for the serialized LangChain object format
        if isinstance(latest_message, dict) and latest_message.get("id"):
            message_type = latest_message["id"][-1]
            kwargs = latest_message.get("kwargs", {})
            content = kwargs.get("content", "")

            if message_type == "AIMessage":
                tool_calls = kwargs.get("tool_calls", [])
                if tool_calls:
                    for tool_call in tool_calls:
                        tool_name = tool_call.get("name")
                        tool_args = tool_call.get("args", {})
                        print(
                            f"  └─ ⚙️  **Calling Tool:** `{tool_name}` with arguments: `{tool_args}`"
                        )
                elif content:
                    print(f"  └─ 💬 **Final Response:** {content}")

            elif message_type == "ToolMessage":
                tool_name = kwargs.get("name")
                print(f"  └─ 🛠️  **Tool Result for `{tool_name}`:** {content}")

            elif message_type == "HumanMessage":
                print(f"  └─ 👤 **Received Input:** {content}")

        # Fallback for the simpler dictionary format (e.g., from tool results)
        elif isinstance(latest_message, dict) and latest_message.get("role"):
            role = latest_message.get("role")
            content = latest_message.get("content", "")
            if role == "tool":
                tool_name = latest_message.get("name")
                print(f"  └─ 🛠️  **Tool Result for `{tool_name}`:** {content}")
            else:
                print(f"  └─ Message (Role: {role}): {content}")
        else:
            print(f"  └─ Unrecognized message format: {latest_message}")

        print("--------------------------------------------------")


# Your existing code to get the agent
agent = agent_engines.get("2664978691217424384")

print("agent operations:", agent.operation_schemas())
print("agent name:", agent.display_name)
print("\n--- Agent Execution Log ---")

# Stream and pretty-print each step
for chunk in agent.stream_query(  # type: ignore[call-arg]
    input={
        "messages": [
            {
                "role": "user",
                "content": "hi, I want to incorporate chennai super kings",
            },
        ]
    }
):
    # The chunk from stream_query is already a dictionary thanks to `dumpd`
    pretty_print_agent_step(chunk)

print("✅ Agent run complete.")
