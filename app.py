# app.py — Sentinel AI Streamlit UI

import streamlit as st
import requests

# ─────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Sentinel AI",
    page_icon="🛡️",
    layout="centered"
)

# ─────────────────────────────────────────
# Header
# ─────────────────────────────────────────
st.title("🛡️ Sentinel AI")
st.subheader("Fraud Investigation Agent for Fintech Compliance Teams")
st.divider()

# ─────────────────────────────────────────
# Sidebar — Available Transactions
# ─────────────────────────────────────────
st.sidebar.title("📋 Available Transactions")
st.sidebar.markdown("Use these IDs to test:")

transactions = {
    "TXN-1001": "✅ Normal   — ₹2,500",
    "TXN-1002": "⚠️ Suspicious — ₹95,000",
    "TXN-1003": "🔴 High Risk  — ₹1,50,000",
    "TXN-1004": "✅ Normal   — ₹1,200",
    "TXN-1005": "🔴 High Risk  — ₹5,00,000",
    "TXN-1006": "✅ Normal   — ₹800",
    "TXN-1007": "⚠️ Suspicious — ₹75,000",
}

for txn_id, description in transactions.items():
    st.sidebar.code(txn_id)
    st.sidebar.caption(description)

st.sidebar.divider()
st.sidebar.info("💡 Copy any Transaction ID and paste it in the input box")

# ─────────────────────────────────────────
# Main Input Section
# ─────────────────────────────────────────
st.markdown("### 🔍 Investigate a Transaction")

transaction_id = st.text_input(
    label="Enter Transaction ID",
    placeholder="e.g. TXN-1003",
    help="Enter the transaction ID you want to investigate"
)

investigate_btn = st.button(
    "🔍 Investigate",
    type="primary",
    use_container_width=True
)

st.divider()

# ─────────────────────────────────────────
# Investigation Logic
# ─────────────────────────────────────────
if investigate_btn:

    # Validate input
    if not transaction_id.strip():
        st.warning("⚠️ Please enter a Transaction ID first!")

    else:
        # Show loading spinner
        with st.spinner(f"🤖 SentinelAI is investigating {transaction_id}..."):
            try:
                # Call FastAPI backend
                response = requests.post(
                    "http://localhost:8000/investigate",
                    json={"transaction_id": transaction_id.strip()}
                )

                # Handle response
                if response.status_code == 200:
                    data = response.json()
                    report = data["report"]

                    # Show success
                    st.success("✅ Investigation Complete!")

                    # Determine risk level for styling
                    if "HIGH RISK" in report:
                        st.error("🔴 HIGH RISK Transaction Detected!")
                    elif "SUSPICIOUS" in report:
                        st.warning("⚠️ Suspicious Transaction Detected!")
                    else:
                        st.success("✅ Transaction appears Normal")

                    # Display Report
                    st.markdown("### 📋 Investigation Report")
                    st.code(report, language=None)

                    # Download Button
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"sentinel_report_{transaction_id}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                else:
                    st.error(f"❌ API Error: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure FastAPI is running!")
                st.code("python main.py", language="bash")

            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# ─────────────────────────────────────────
# Footer
# ─────────────────────────────────────────
st.divider()
st.caption("🛡️ Sentinel AI — Powered by Claude AI + LangChain | Demo Version 1.0")