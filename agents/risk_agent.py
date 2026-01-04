from utils.llm import call_llm

def risk_agent(state: dict) -> dict:
    prompt = f"""
You are an enterprise risk analyst.

Compliance Findings:
{state['compliance_findings']}

Assess:
- Risk Level
- Business Impact
- Regulatory Exposure
"""

    analysis = call_llm(prompt)

    if "HIGH" in analysis.upper():
        risk_level = "HIGH"
    elif "LOW" in analysis.upper():
        risk_level = "LOW"
    else:
        risk_level = "MEDIUM"

    trace = state.get("agent_trace", [])
    trace.append({
        "agent": "Risk Analysis Agent",
        "status": "Completed",
        "summary": f"Risk classified as {risk_level}"
    })

    return {
        **state,
        "risk_analysis": analysis,
        "risk_level": risk_level,
        "agent_trace": trace,
        "status": "RISK_ANALYZED"
    }
