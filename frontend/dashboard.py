import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def show_dashboard(fastapi_base_url: str):
    st.title("📊 ShopNova Analytics Dashboard")
    st.markdown("---")

    try:
        res = requests.get(f"{fastapi_base_url}/analytics/")
        data = res.json()
    except:
        st.error("Cannot connect to backend.")
        return

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Queries", data["total_queries"])
    col2.metric("RAG Hits", data["rag_hits"])
    col3.metric("Web Search Used", data["web_hits"])
    col4.metric("Avg Response Time", f"{data['avg_response_time']}s")

    st.markdown("---")

    # RAG vs Web chart
    st.subheader("🔍 RAG vs Web Search")
    chart_data = pd.DataFrame({
        "Source": ["RAG", "Web Search"],
        "Count": [data["rag_hits"], data["web_hits"]]
    })
    fig = px.bar(chart_data, x="Source", y="Count", color="Source",
                 color_discrete_map={"RAG": "#4CAF50", "Web Search": "#2196F3"})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Recent queries table
    st.subheader("🕐 Recent Queries")
    if data["recent_queries"]:
        df = pd.DataFrame(data["recent_queries"],
                         columns=["Query", "Route", "Used Web", "Response Time", "Timestamp"])
        df["Used Web"] = df["Used Web"].apply(lambda x: "✅" if x else "❌")
        df["Response Time"] = df["Response Time"].apply(lambda x: f"{round(x, 2)}s")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No queries yet.")