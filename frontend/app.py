# rag_agent_app/frontend/app.py
import requests
import streamlit as st
import json

from config import FRONTEND_CONFIG
from session_manager import init_session_state
from ui_component import (
    display_header,
    render_document_upload_section,
    render_agent_settings_section,
    display_chat_history,
    display_trace_events
)
from backend_api import chat_with_backend_agent
from dashboard import show_dashboard


def main():
    init_session_state()
    fastapi_base_url = FRONTEND_CONFIG["FASTAPI_BASE_URL"]
    display_header()

    # Navigation في الـ sidebar
    page = st.sidebar.radio("📌 Navigation", ["💬 Chat", "📊 Dashboard"])

    if page == "📊 Dashboard":
        show_dashboard(fastapi_base_url)
    else:
        st.header("Chat with ShopNova Agent")
        display_chat_history()

        if prompt := st.chat_input("Your message"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        agent_response, trace_events = chat_with_backend_agent(
                            fastapi_base_url,
                            st.session_state.session_id,
                            prompt,
                            st.session_state.web_search_enabled
                        )
                        st.markdown(agent_response)
                        st.session_state.messages.append({"role": "assistant", "content": agent_response})
                        display_trace_events(trace_events)

                    except requests.exceptions.ConnectionError:
                        st.error("Could not connect to the FastAPI backend. Please ensure it's running.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"An error occurred with the request: {e}")
                    except json.JSONDecodeError:
                        st.error("Received an invalid response from the backend.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()