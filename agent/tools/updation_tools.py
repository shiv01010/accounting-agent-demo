from langchain_core.tools import tool


@tool
def update_company_address(address: str) -> str:
    """Updates the registered address of the company."""
    print(f"--- new address of the company is:{address} ---")
    return f"Successfully updated the company address to '{address}'."


@tool
def update_company_registered_name(name: str) -> str:
    """Updates the registered name of the company."""
    print(f"--- Updating company name to: {name} ---")
    return f"Successfully updated the company name to '{name}'."


@tool
def update_company_director_name(director_name: str) -> str:
    """Updates the director's name of the company."""
    print(f"--- Updating director's name to: {director_name} ---")
    return f"Successfully updated the director's name to '{director_name}'."


updation_tool_list = [
    update_company_address,
    update_company_registered_name,
    update_company_director_name,
]
