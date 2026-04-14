# tools.py — Agent Tools for Sentinel AI

from data import transactions, watchlist_accounts, watchlist_names

# ─────────────────────────────────────────
# TOOL 1: Fetch Transaction by ID
# ─────────────────────────────────────────
def get_transaction(transaction_id: str) -> dict:
    """
    Fetches a transaction by its ID
    """
    for txn in transactions:
        if txn["transaction_id"] == transaction_id:
            return txn
    return {"error": f"Transaction {transaction_id} not found"}


# ─────────────────────────────────────────
# TOOL 2: Get All Transactions by Account
# ─────────────────────────────────────────
def get_account_history(account_id: str) -> list:
    """
    Fetches all transactions for a given account
    """
    history = [
        txn for txn in transactions
        if txn["account_id"] == account_id
    ]
    if history:
        return history
    return [{"error": f"No transactions found for {account_id}"}]


# ─────────────────────────────────────────
# TOOL 3: Check Watchlist
# ─────────────────────────────────────────
def check_watchlist(account_id: str, name: str) -> dict:
    """
    Checks if account or name is in the fraud watchlist
    """
    flagged_account = account_id in watchlist_accounts
    flagged_name = name in watchlist_names

    if flagged_account or flagged_name:
        return {
            "is_flagged": True,
            "reason": f"Account '{account_id}' or Name '{name}' is on the fraud watchlist"
        }
    return {
        "is_flagged": False,
        "reason": "No watchlist match found"
    }


# ─────────────────────────────────────────
# TOOL 4: Calculate Risk Score
# ─────────────────────────────────────────
def calculate_risk_score(transaction_id: str) -> dict:
    """
    Calculates a fraud risk score based on rules
    """
    txn = get_transaction(transaction_id)

    if "error" in txn:
        return txn

    score = 0
    reasons = []

    # Rule 1 — High amount
    if txn["amount"] >= 100000:
        score += 40
        reasons.append("Very high transaction amount")
    elif txn["amount"] >= 50000:
        score += 25
        reasons.append("High transaction amount")

    # Rule 2 — Odd hours (between 12AM and 6AM)
    hour = int(txn["timestamp"].split(" ")[1].split(":")[0])
    if 0 <= hour <= 6:
        score += 30
        reasons.append("Transaction at odd hours")

    # Rule 3 — Watchlist check
    watchlist = check_watchlist(
        txn["receiver_account"],
        txn["name"]
    )
    if watchlist["is_flagged"]:
        score += 30
        reasons.append("Receiver or sender on watchlist")

    # Rule 4 — Unknown location
    if txn["location"].lower() == "unknown":
        score += 20
        reasons.append("Transaction from unknown location")

    # Determine risk level
    if score >= 70:
        risk_level = "🔴 HIGH RISK"
    elif score >= 40:
        risk_level = "⚠️ SUSPICIOUS"
    else:
        risk_level = "✅ NORMAL"

    return {
        "transaction_id": transaction_id,
        "risk_score": min(score, 100),
        "risk_level": risk_level,
        "reasons": reasons
    }