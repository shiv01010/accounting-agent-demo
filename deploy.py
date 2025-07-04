# deploy.py
import os
from dotenv import load_dotenv
from vertexai import agent_engines
import google.auth.exceptions
from typing import Callable, Sequence, cast
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory

# Import the AccountingAgent class
from agent.accounting_agent import AccountingAgent

load_dotenv(override=True)

safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}


def deploy_multi_agent_system():
    """
    Deploys the custom multi-agent supervisor graph to Vertex AI.
    This is the correct method for advanced, custom-built LangGraph applications.
    """
    project_id = os.getenv("GCLOUD_PROJECT")
    location = os.getenv("GCLOUD_REGION")
    staging_bucket = os.getenv("GCS_BUCKET")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL")
    supabase_url = os.getenv("SUPABASE_URL", "https://your-supabase-url.supabase.co")
    supabase_key = os.getenv("SUPABASE_API_KEY", "your-supabase-key")

    env_vars = {
        "OPENAI_API_KEY": openai_api_key,
        "OPENAI_MODEL": model_name,
        "SUPABASE_URL": supabase_url,
        "SUPABASE_API_KEY": supabase_key,
        "GCLOUD_PROJECT": project_id,
        "GCLOUD_REGION": location,
        "GCS_BUCKET": staging_bucket,
    }

    # Ensure all required environment variables are set, including staging_bucket
    if not all(
        [
            project_id,
            location,
            staging_bucket,
            openai_api_key,
            model_name,
            supabase_url,
            supabase_key,
        ]
    ):
        raise ValueError(
            "GCLOUD_PROJECT, GCLOUD_REGION, GCS_BUCKET, OPENAI_API_KEY,OPENAI_MODEL,SUPABASE_URL,SUPABASE_KEY must be set in .env file"
        )
    # Type narrowing after validation
    assert (
        project_id is not None
        and location is not None
        and staging_bucket is not None
        and openai_api_key is not None
    )
    # staging_bucket is now guaranteed to be str
    staging_bucket = cast(str, staging_bucket)

    # Set up the AccountingAgent using openAI Chat and LangGraph

    if not model_name:
        raise ValueError("OPENAI_MODEL must be set in .env file")
    # Define any agent tools (import or list your tool callables here)
    tools: Sequence[Callable] = []
    agent = AccountingAgent(
        model=model_name,
        tools=tools,
        project=project_id,
        location=location,
        bucket=staging_bucket,
    )
    agent.set_up()

    # Read and filter base requirements
    requirements = [
        "google-cloud-aiplatform[agent_engines,langgraph]",
        "langchain-google-vertexai",
        "langgraph",
        "langchain",
        "langchain_openai",
        "langchain_core",
        "python-dotenv",
        "supabase",
        "cloudpickle",
    ]
    # The 'extra_packages' argument packages your entire 'agent' source directory.
    extra_packages = ["agent"]

    print("Deploying custom multi-agent graph to Vertex AI...")

    try:
        remote_engine = agent_engines.AgentEngine.create(
            agent_engine=agent,
            display_name="Accounting Multi-Agent System",
            requirements=requirements,
            extra_packages=extra_packages,
            description="A multi-agent system for accounting tasks, including incorporation, updation, maintenance",
            env_vars=env_vars,
        )
    except google.auth.exceptions.RefreshError as e:
        raise RuntimeError(
            "Authentication error: Token has expired or revoked. "
            "Please reauthenticate by running 'gcloud auth application-default login' "
            "or set service account credentials."
        ) from e

    print("\nMulti-agent system deployment initiated successfully!")
    print(f"Resource Name: {remote_engine.resource_name}")
    print("You can monitor the deployment status in the Google Cloud Console.")


if __name__ == "__main__":
    deploy_multi_agent_system()
