import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="K8s Health Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Kubernetes Health Assistant")
st.caption("Real-time cluster observability powered by MCP")

# -------------------------------
# Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("⚡ Quick Actions")

sidebar_prompt = None

if st.sidebar.button("Cluster Health"):
    sidebar_prompt = "cluster health"

if st.sidebar.button("CPU Health"):
    sidebar_prompt = "cpu health"

if st.sidebar.button("Memory Health"):
    sidebar_prompt = "memory health"

if st.sidebar.button("Namespace Health"):
    sidebar_prompt = "namespace health"

# -------------------------------
# UI Helpers
# -------------------------------
def render_namespace_table(namespaces):
    st.subheader("📦 Namespace Health")

    namespaces = sorted(namespaces, key=lambda x: x["score"])

    critical_count = sum(1 for ns in namespaces if ns["status"] == "critical")

    if critical_count > 0:
        st.error(f"🚨 {critical_count} namespaces are in CRITICAL state")
    else:
        st.success("✅ All namespaces healthy")

    table_data = []

    for ns in namespaces:
        emoji = {
            "healthy": "🟢 Healthy",
            "warning": "🟡 Warning",
            "critical": "🔴 Critical"
        }.get(ns["status"], ns["status"])

        table_data.append({
            "Namespace": ns["namespace"],
            "Score": round(ns["score"], 2),
            "Status": emoji
        })

    st.dataframe(table_data, use_container_width=True)


def render_cpu_memory(result):
    col1, col2, col3 = st.columns(3)

    col1.metric("Usage %", f"{round(result['usage_percent'], 2)}%")
    col2.metric("Score", result.get("score", 0))
    col3.metric("Status", result.get("status", "").upper())

    if result.get("status") == "critical":
        st.error("🚨 Resource usage is CRITICAL")
    elif result.get("status") == "warning":
        st.warning("⚠️ Resource usage is HIGH")
    else:
        st.success("✅ Resource usage is NORMAL")


def render_cluster(result):
    col1, col2 = st.columns(2)

    col1.metric("Cluster Score", result["cluster_score"])
    col2.metric("Status", result["status"].upper())

    if result["status"] == "critical":
        st.error("🚨 Cluster health is CRITICAL")
    elif result["status"] == "warning":
        st.warning("⚠️ Cluster health is DEGRADED")
    else:
        st.success("✅ Cluster is healthy")


def render_response(data):
    result = data.get("result", {})

    if "usage_percent" in result:
        render_cpu_memory(result)

    elif "cluster_score" in result:
        render_cluster(result)

    elif "namespaces" in result:
        render_namespace_table(result["namespaces"])

    else:
        st.json(result)


# -------------------------------
# Chat History (FIXED)
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        # 👇 Re-render structured responses
        if msg["role"] == "assistant" and isinstance(msg["content"], dict):
            render_response(msg["content"])
        else:
            st.markdown(msg["content"])


# -------------------------------
# Input
# -------------------------------
user_prompt = st.chat_input("Ask about your cluster...")
prompt = user_prompt or sidebar_prompt


# -------------------------------
# Execute
# -------------------------------
if prompt:

    # Avoid duplicate rerun issues
    if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["content"] != prompt:

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.spinner("🔍 Analyzing cluster..."):
                response = requests.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=10
                )

            if response.status_code != 200:
                with st.chat_message("assistant"):
                    st.error(f"❌ API Error: {response.text}")

            else:
                data = response.json()

                # 👇 Render UI immediately
                with st.chat_message("assistant"):
                    render_response(data)

                # 👇 STORE FULL RESPONSE (KEY FIX)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data
                })

        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"❌ Error: {str(e)}")