def ingestion_agent(state: dict) -> dict:
    text = state["document_text"]

    trace = state.get("agent_trace", [])
    trace.append({
        "agent": "Document Ingestion Agent",
        "status": "Completed",
        "summary": f"Document ingested ({len(text.split())} words)"
    })

    return {
        **state,
        "parsed_document": {
            "content": text,
            "word_count": len(text.split()),
            "scope_note": (
                "Assessment is based solely on the provided document. "
                "No independent verification performed."
            ),
            "status": "INGESTED"
        },
        "agent_trace": trace
    }
