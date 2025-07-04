from typing import Callable, Sequence, Iterable


class AccountingAgent:
    def __init__(
        self,
        model: str,
        tools: Sequence[Callable],
        project: str,
        location: str,
        bucket: str,
    ):
        self.model_name = model
        self.tools = tools
        self.project = project
        self.location = location
        self.bucket = bucket

    def set_up(self):
        import vertexai

        # Use the supervisor_agent orchestration graph
        from agent.supervisor_agent import supervisor_graph

        # Initialize Vertex AI with the specified project and location
        vertexai.init(
            project=self.project, location=self.location, staging_bucket=self.bucket
        )

        # No longer storing graph on the instance to avoid pickling issues

    def query(self, **kwargs):
        # Import and invoke the graph at call time to avoid pickling locks
        from agent.supervisor_agent import supervisor_graph

        return supervisor_graph.invoke(**kwargs)

    def stream_query(self, **kwargs) -> Iterable:
        from langchain.load.dump import dumpd
        from agent.supervisor_agent import supervisor_graph

        for chunk in supervisor_graph.stream(
            **kwargs,
        ):
            yield dumpd(chunk)
