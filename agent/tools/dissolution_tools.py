from langchain_core.tools import tool


@tool
def mark_company_for_dissolution(company_id: str) -> str:
    """Marks a company for dissolution."""
    print(f"--- Marking company {company_id} for dissolution ---")
    return f"Company {company_id} has been marked for dissolution."


dissolution_tool_list = [mark_company_for_dissolution]
