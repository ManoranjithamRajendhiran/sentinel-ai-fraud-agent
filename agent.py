# agent.py — Sentinel AI (Compatible with LangChain 1.2.15)

import os
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from tools import (
    get_transaction,
    get_account_history,
    check_watchlist,
    calculate_risk_score
)

# ─────────────────────────────────────────
# Load Environment Variables
# ─────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────
# Initialize Claude LLM
# ─────────────────────────────────────────
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0
)

# ─────────────────────────────────────────
# Wrap Tools for LangChain
# ─────────────────────────────────────────

@tool
def fetch_transaction(transaction_id: str) -> dict:
    """Fetches a transaction record by transaction ID"""
    return get_transaction(transaction_id)

@tool
def fetch_account_history(account_id: str) -> list:
    """Fetches all transactions for a given account ID"""
    return get_account_history(account_id)

@tool
def verify_watchlist(account_id: str, name: str) -> dict:
    """Checks if an account ID or person name is on the fraud watchlist"""
    return check_watchlist(account_id, name)

@tool
def get_risk_score(transaction_id: str) -> dict:
    """Calculates fraud risk score for a given transaction ID"""
    return calculate_risk_score(transaction_id)

# ─────────────────────────────────────────
# Register Tools
# ─────────────────────────────────────────
tools = [
    fetch_transaction,
    fetch_account_history,
    verify_watchlist,
    get_risk_score
]

# ─────────────────────────────────────────
# Bind Tools to Claude
# ─────────────────────────────────────────
llm_with_tools = llm.bind_tools(tools)

# ─────────────────────────────────────────
# System Prompt
# ─────────────────────────────────────────
SYSTEM_PROMPT = """
You are SentinelAI, an expert fraud investigation agent
for a fintech payments company.

When given a transaction ID, you must:
1. Fetch the transaction details
2. Check the account transaction history
3. Verify if sender or receiver is on the watchlist
4. Calculate the fraud risk score
5. Generate a clear investigation report

Always end with a structured report in this format:

═══════════════════════════════════════
       SENTINEL AI — INVESTIGATION REPORT
═══════════════════════════════════════
Transaction ID   : <id>
Account ID       : <id>
Account Holder   : <name>
Amount           : ₹<amount>
Location         : <location>
Transaction Type : <type>
Timestamp        : <time>
───────────────────────────────────────
Watchlist Status : <flagged/clear>
Risk Score       : <score>/100
Risk Level       : <level>
───────────────────────────────────────
Key Findings     :
  • <finding 1>
  • <finding 2>
  • <finding 3>
───────────────────────────────────────
Recommendation   : <action>
═══════════════════════════════════════
"""

# ─────────────────────────────────────────
# Tool Executor
# ─────────────────────────────────────────
tool_map = {
    "fetch_transaction"    : fetch_transaction,
    "fetch_account_history": fetch_account_history,
    "verify_watchlist"     : verify_watchlist,
    "get_risk_score"       : get_risk_score
}

def execute_tool(tool_call: dict) -> str:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    if tool_name in tool_map:
        result = tool_map[tool_name].invoke(tool_args)
        print(f"\n🔧 Tool Called : {tool_name}")
        print(f"📥 Input       : {tool_args}")
        print(f"📤 Output      : {result}")
        return str(result)

    return f"Tool {tool_name} not found"

# ─────────────────────────────────────────
# Main Investigation Function
# ─────────────────────────────────────────
def investigate(transaction_id: str) -> str:
    print(f"\n{'='*50}")
    print(f"🔍 Starting Investigation : {transaction_id}")
    print(f"{'='*50}")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Investigate transaction ID: {transaction_id} and give full fraud investigation report.")
    ]

    # Agentic loop
    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            print(f"\n⚙️  Calling {len(response.tool_calls)} tool(s)...")
            for tool_call in response.tool_calls:
                result = execute_tool(tool_call)
                messages.append(
                    ToolMessage(
                        content=result,
                        tool_call_id=tool_call["id"]
                    )
                )
        else:
            print(f"\n✅ Investigation Complete!")
            return response.content


# ─────────────────────────────────────────
# Quick Test
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n🔴 Test 1 — High Risk Transaction")
    report = investigate("TXN-1003")
    print(report)

    print("\n✅ Test 2 — Normal Transaction")
    report = investigate("TXN-1004")
    print(report)