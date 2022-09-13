from datetime import datetime
def journalEntry(item) -> dict:
    return {
        "id": str(item["_id"]),
        "date_entry": str(item["date_entry"]),
        "journal": str(item["journal"]),
        "ref": str(item["ref"]),
        "descriptions": str(item["descriptions"]),
        "acoount_number": str(item["acoount_number"]),
        "account_disc": str(item["account_disc"]),
        "debit_amount": str(item["debit_amount"]),
        "credit_amount": str(item["credit_amount"]),
        "due_date_apv": str(item["due_date_apv"]),
        "terms_days": str(item["terms_days"]),
        "supplier/Client": str(item["supplier/Client"]),
        "user": str(item["user"]),
        "created": str(item["created"])
    }

def journalEntrys(entity) -> list:
    return [journalEntry(item) for item in entity] 