def requires_human_approval(risk_level: str) -> bool:
    """
    Enforces mandatory human decision for medium/high risk.
    """
    return risk_level in ["MEDIUM", "HIGH"]
