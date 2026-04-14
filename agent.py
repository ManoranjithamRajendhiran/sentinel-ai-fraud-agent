# agent.py — Sentinel AI Fraud Investigation Agent

import os
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate

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
# Step 1 — Initialize Claude LLM
# ─────────────────────────────────────────
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0
)

# ─────────────────────────────────────────
# Step 2 — Wrap Tools for LangChain
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
# Step 3 — Register All Tools
# ─────────────────────────────────────────
tools = [
    fetch_transaction,
    fetch_account_history,
    verify_watchlist,
    get_risk_score
]

# ─────────────────────────────────────────
# Step 4 — Define Agent System Prompt
# ─────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
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
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# ─────────────────────────────────────────
# Step 5 — Create the Agent
# ─────────────────────────────────────────
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# ─────────────────────────────────────────
# Step 6 — Create Agent Executor
# ─────────────────────────────────────────
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ─────────────────────────────────────────
# Step 7 — Main Investigation Function
# ─────────────────────────────────────────
def investigate(transaction_id: str) -> str:
    """
    Main function to investigate a transaction
    """
    response = agent_executor.invoke({
        "input": f"Please investigate transaction ID: {transaction_id} and provide a full fraud investigation report."
    })
    return response["output"]


# ─────────────────────────────────────────
# Quick Test
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n🔍 Investigating TXN-1003 (High Risk)...\n")
    report = investigate("TXN-1003")
    print(report)

    print("\n🔍 Investigating TXN-1004 (Normal)...\n")
    report = investigate("TXN-1004")
    print(report)