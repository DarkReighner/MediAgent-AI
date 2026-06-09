from langgraph.graph import StateGraph
from app.agent_state import MediAgentState
from app.agents import (
    extraction_agent,
    retrieval_agent,
    decision_agent
)

builder = StateGraph(MediAgentState)

builder.add_node(
    "extract",
    extraction_agent
)

builder.add_node(
    "retrieve",
    retrieval_agent
)

builder.add_node(
    "decide",
    decision_agent
)

builder.set_entry_point("extract")

builder.add_edge(
    "extract",
    "retrieve"
)

builder.add_edge(
    "retrieve",
    "decide"
)

graph = builder.compile()