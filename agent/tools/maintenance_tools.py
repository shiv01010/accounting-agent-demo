from langchain_core.tools import tool


@tool
def file_annual_return(company_id: str) -> str:
    """Files the annual compliance return for a given company ID."""
    print(f"--- Filing annual return for: {company_id} ---")
    return f"Annual return for company {company_id} has been filed successfully."


maintenance_tool_list = [file_annual_return]
