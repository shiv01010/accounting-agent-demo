from langchain_core.tools import tool
from ..db.supabase import get_supabase_client


@tool
def check_company_name_availability(company_name: str) -> str:
    """Checks if a company name is available for registration using Supabase."""
    supabase = get_supabase_client()
    response = (
        supabase.table("company")
        .select("company_name")
        .eq("company_name", company_name)
        .execute()
    )
    # Handle different response formats
    data = (
        response.data
        if hasattr(response, "data")
        else (response[0] if isinstance(response, list) else None)
    )
    if data and len(data) > 0:
        return f"The name '{company_name}' is already registered."
    return f"The name '{company_name}' is available."


@tool
def register_company(company_name: str) -> str:
    """Registers a new company with the given name in Supabase."""
    supabase = get_supabase_client()
    response = (
        supabase.table("company").insert({"company_name": company_name}).execute()
    )
    data = (
        response.data
        if hasattr(response, "data")
        else (response[0] if isinstance(response, list) else None)
    )
    if not data:
        return "Failed to register company."
    # Extract inserted company ID
    company_id = data[0].get("id") if isinstance(data, list) else data.get("id")
    return f"Successfully registered '{company_name}'. Company ID is {company_id}."


@tool
def collect_incorporation_details() -> str:
    """Collects details required for company incorporation."""

    return (
        "Please provide the following details for company incorporation:\n"
        "1. Company Name\n"
        "2. Company Type (e.g., Private Limited, Public Limited)\n"
        "3. Registered Address\n"
        "4. Director(s) Information (Name, Address, etc.)\n"
        "5. Shareholder(s) Information (Name, Address, etc.)\n"
        "6. Any other relevant information."
    )


incorporation_tool_list = [check_company_name_availability, register_company]
