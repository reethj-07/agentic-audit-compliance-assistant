import streamlit as st
from graph import build_graph
from utils.parsers import parse_pdf
from utils.pdf_generator import generate_audit_pdf

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Agentic Audit Assistant",
    layout="wide"
)

st.title("🏛️ Agentic Audit & Compliance Assistant")

# --------------------------------------------------
# Initialize session state
# --------------------------------------------------
if "audit_result" not in st.session_state:
    st.session_state.audit_result = None

if "audit_run" not in st.session_state:
    st.session_state.audit_run = False

if "approved" not in st.session_state:
    st.session_state.approved = False

if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None

# --------------------------------------------------
# File upload
# --------------------------------------------------
uploaded = st.file_uploader(
    "Upload Audit / Policy Document",
    type=["pdf", "txt"]
)

if uploaded:
    # ✅ Reset state ONLY if a NEW file is uploaded
    if uploaded.name != st.session_state.last_uploaded_filename:
        st.session_state.audit_result = None
        st.session_state.audit_run = False
        st.session_state.approved = False
        st.session_state.last_uploaded_filename = uploaded.name

    if uploaded.type == "application/pdf":
        document_text = parse_pdf(uploaded)
    else:
        document_text = uploaded.read().decode("utf-8")

    st.success("📄 Document ingested successfully")

    # --------------------------------------------------
    # Run audit button
    # --------------------------------------------------
    if st.button("Run Agentic Audit"):
        graph = build_graph()

        result = graph.invoke({
            "document_text": document_text
        })

        st.session_state.audit_result = result
        st.session_state.audit_run = True

# --------------------------------------------------
# Display results
# --------------------------------------------------
if st.session_state.audit_run and st.session_state.audit_result:
    result = st.session_state.audit_result

    # --------------------------------------------------
    # Risk summary
    # --------------------------------------------------
    st.subheader("🔎 Risk Level")

    if result["risk_level"] == "HIGH":
        st.error("HIGH RISK")
    elif result["risk_level"] == "MEDIUM":
        st.warning("MEDIUM RISK")
    else:
        st.success("LOW RISK")

    # --------------------------------------------------
    # Agent Execution Trace
    # --------------------------------------------------
    st.subheader("🧭 Agent Execution Trace")

    for step in result.get("agent_trace", []):
        with st.expander(step["agent"]):
            st.markdown(f"""
**Status:** {step['status']}  
**Summary:** {step['summary']}
""")

    # --------------------------------------------------
    # Human-in-the-loop approval
    # --------------------------------------------------
    if result["risk_level"] in ["MEDIUM", "HIGH"]:
        st.session_state.approved = st.checkbox(
            "I approve proceeding with report generation",
            value=st.session_state.approved
        )

        if st.session_state.approved:
            st.success("Human approval recorded")

            st.subheader("📄 Audit Report")
            st.write(result["final_report"])

            pdf_bytes = generate_audit_pdf(result["final_report"])

            st.download_button(
                label="⬇️ Download Audit Report (PDF)",
                data=pdf_bytes,
                file_name="audit_report.pdf",
                mime="application/pdf"
            )

    else:
        st.subheader("📄 Audit Report")
        st.write(result["final_report"])

        pdf_bytes = generate_audit_pdf(result["final_report"])

        st.download_button(
            label="⬇️ Download Audit Report (PDF)",
            data=pdf_bytes,
            file_name="audit_report.pdf",
            mime="application/pdf"
        )
