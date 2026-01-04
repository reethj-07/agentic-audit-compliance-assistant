from utils.llm import call_llm

def report_agent(state: dict) -> dict:
    prompt = f"""
Generate a formal internal audit report with the following sections:

1. Executive Summary
   - High-level overview of findings
   - Explicit statement of overall risk level (LOW / MEDIUM / HIGH)
   - Brief justification for the risk level

2. Scope & Limitations
   - Clarify that the assessment is based only on the provided document
   - Note that no independent control testing was performed

3. Compliance Gaps (with Evidence)
   - List each compliance gap
   - Include supporting document evidence or explicitly state when evidence is insufficient

4. Risk Assessment
   - Overall Risk Level
   - Business Impact
   - Regulatory Exposure (generalized, no specific regulations unless stated in the document)
   - Justification for Risk Rating
   - Confidence Level (Low / Moderate / High), based on scope and evidence

5. Recommendations
   - Actionable remediation steps

6. AI Decision Boundaries
   - The system applies predefined compliance rules and uses a language model to assist in identifying potential gaps
   - The system does not perform regulatory interpretation or final decision-making
   - Risk ratings are advisory and require human review and approval

7. Disclaimer
   - For internal use only
   - Not a substitute for a statutory or regulatory audit

Input:
{state}

Tone:
- Professional
- Conservative
- Suitable for senior management and auditors
"""

    report = call_llm(prompt)

    trace = state.get("agent_trace", [])
    trace.append({
        "agent": "Report Generation Agent",
        "status": "Completed",
        "summary": "Formal audit report generated"
    })

    return {
        **state,
        "final_report": report,
        "agent_trace": trace,
        "status": "REPORT_GENERATED"
    }
