from langgraph.graph import StateGraph, END

from agents.ingestion_agent import ingestion_agent
from agents.compliance_agent import compliance_agent
from agents.risk_agent import risk_agent
from agents.report_agent import report_agent
from guardrails.checks import requires_human_approval


def build_graph():
    workflow = StateGraph(dict)

    # Register agents
    workflow.add_node("ingestion", ingestion_agent)
    workflow.add_node("compliance", compliance_agent)
    workflow.add_node("risk", risk_agent)
    workflow.add_node("report", report_agent)

    # Entry point
    workflow.set_entry_point("ingestion")

    # Normal flow
    workflow.add_edge("ingestion", "compliance")
    workflow.add_edge("compliance", "risk")

    # Conditional routing (Human-in-the-loop)
    def approval_router(state):
        if requires_human_approval(state["risk_level"]):
            return "report"   # still generate, but gated by UI
        return "report"

    workflow.add_conditional_edges(
        "risk",
        approval_router
    )

    # End
    workflow.add_edge("report", END)

    return workflow.compile()
