# data.py — Mock Transaction Data for Sentinel AI

transactions = [
    {
        "transaction_id": "TXN-1001",
        "account_id": "ACC-101",
        "name": "Rahul Sharma",
        "amount": 2500,
        "currency": "INR",
        "location": "Chennai",
        "receiver_account": "ACC-901",
        "timestamp": "2024-01-15 09:30:00",
        "transaction_type": "NEFT",
        "status": "completed"
    },
    {
        "transaction_id": "TXN-1002",
        "account_id": "ACC-102",
        "name": "Priya Mehta",
        "amount": 95000,
        "currency": "INR",
        "location": "Mumbai",
        "receiver_account": "ACC-999",
        "timestamp": "2024-01-15 02:15:00",
        "transaction_type": "IMPS",
        "status": "completed"
    },
    {
        "transaction_id": "TXN-1003",
        "account_id": "ACC-103",
        "name": "John Doe",
        "amount": 150000,
        "currency": "INR",
        "location": "Delhi",
        "receiver_account": "ACC-777",
        "timestamp": "2024-01-15 03:45:00",
        "transaction_type": "RTGS",
        "status": "completed"
    },
    {
        "transaction_id": "TXN-1004",
        "account_id": "ACC-104",
        "name": "Sneha Patel",
        "amount": 1200,
        "currency": "INR",
        "location": "Coimbatore",
        "receiver_account": "ACC-202",
        "timestamp": "2024-01-15 11:00:00",
        "transaction_type": "UPI",
        "status": "completed"
    },
    {
        "transaction_id": "TXN-1005",
        "account_id": "ACC-105",
        "name": "Ahmed Khan",
        "amount": 500000,
        "currency": "INR",
        "location": "Hyderabad",
        "receiver_account": "ACC-666",
        "timestamp": "2024-01-15 01:30:00",
        "transaction_type": "NEFT",
        "status": "completed"
    },
    {
        "transaction_id": "TXN-1006",
        "account_id": "ACC-106",
        "name": "Divya Krishnan",
        "amount": 800,
        "currency": "INR",
        "location": "Bangalore",
        "receiver_account": "ACC-303",
        "timestamp": "2024-01-15 10:20:00",
        "transaction_type": "UPI",
        "status": "completed"
    },
    {
        "transaction_id": "TXN-1007",
        "account_id": "ACC-107",
        "name": "Vikram Singh",
        "amount": 75000,
        "currency": "INR",
        "location": "Unknown",
        "receiver_account": "ACC-888",
        "timestamp": "2024-01-15 04:10:00",
        "transaction_type": "IMPS",
        "status": "completed"
    },
]

# Flagged/suspicious accounts watchlist
watchlist_accounts = [
    "ACC-999",
    "ACC-777",
    "ACC-666",
    "ACC-888"
]

# Flagged account holders
watchlist_names = [
    "John Doe",
    "Ahmed Khan"
]