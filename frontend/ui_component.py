# rag_agent_app/frontend/ui_components.py

import streamlit as st
from backend_api import upload_document_to_backend
from session_manager import init_session_state

def display_header():
    st.set_page_config(page_title="ShopNova Support", layout="wide")

    with st.sidebar:
        render_document_upload_section_sidebar()
        render_agent_settings_section()

    st.title("🛍️ ShopNova Support")
    st.markdown("Ask me about orders, returns, shipping, and more.")
    st.markdown("---")

def render_document_upload_section_sidebar():
    st.subheader("📄 Knowledge Base")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="pdf_uploader")
    if st.button("Upload PDF", key="upload_pdf_button"):
        if uploaded_file is not None:
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                try:
                    from config import FRONTEND_CONFIG
                    fastapi_base_url = FRONTEND_CONFIG["FASTAPI_BASE_URL"]
                    upload_data = upload_document_to_backend(fastapi_base_url, uploaded_file)
                    st.success(f"✅ Uploaded! ({upload_data.get('processed_chunks')} pages)")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please choose a PDF first.")
    st.markdown("---")

def render_document_upload_section(fastapi_base_url: str):
    pass  # اتنقلت للـ sidebar

def render_agent_settings_section():
    st.subheader("⚙️ Agent Settings")
    st.session_state.web_search_enabled = st.checkbox(
        "Enable Web Search 🌐",
        value=st.session_state.web_search_enabled,
        help="Enable web search when knowledge base is insufficient."
    )
    st.markdown("---")

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def display_trace_events(trace_events: list):
    if trace_events:
        with st.expander("🔬 Agent Workflow Trace"):
            for event in trace_events:
                icon_map = {
                    'router': "➡️",
                    'rag_lookup': "📚",
                    'web_search': "🌐",
                    'answer': "💡",
                    '__end__': "✅"
                }
                icon = icon_map.get(event['node_name'], "⚙️")
                st.subheader(f"{icon} Step {event['step']}: {event['node_name']}")
                st.write(f"**Description:** {event['description']}")

                if event['node_name'] == 'rag_lookup' and 'sufficiency_verdict' in event['details']:
                    verdict = event['details']['sufficiency_verdict']
                    if verdict == "Sufficient":
                        st.success(f"**RAG Verdict:** {verdict}")
                    else:
                        st.warning(f"**RAG Verdict:** {verdict}")
                    if 'retrieved_content_summary' in event['details']:
                        st.markdown(f"**Summary:** `{event['details']['retrieved_content_summary']}`")
                elif event['node_name'] == 'web_search' and 'retrieved_content_summary' in event['details']:
                    st.markdown(f"**Web Summary:** `{event['details']['retrieved_content_summary']}`")
                elif event['node_name'] == 'router' and 'router_override_reason' in event['details']:
                    st.info(f"**Override:** {event['details']['router_override_reason']}")
                    st.json({"initial": event['details']['initial_decision'], "final": event['details']['final_decision']})
                elif event['details']:
                    st.json(event['details'])
                st.markdown("---")