from utils.llm import call_llm

COMPLIANCE_RULES = """
1. Role-based access control must be enforced
2. Dual approval required for sensitive actions
3. Logging and monitoring must be enabled
4. Logs must be retained for a minimum of 90 days
"""

def compliance_agent(state: dict) -> dict:
    prompt = f"""
You are a senior banking compliance auditor.

Compliance Rules:
{COMPLIANCE_RULES}

Document:
{state['parsed_document']['content']}

Identify compliance gaps with evidence.
"""

    findings = call_llm(prompt)

    trace = state.get("agent_trace", [])
    trace.append({
        "agent": "Compliance Rule Agent",
        "status": "Completed",
        "summary": "Identified compliance gaps and supporting evidence"
    })

    return {
        **state,
        "compliance_findings": findings,
        "agent_trace": trace,
        "status": "COMPLIANCE_CHECKED"
    }
