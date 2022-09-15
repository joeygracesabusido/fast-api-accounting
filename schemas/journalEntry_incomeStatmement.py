from datetime import datetime
def journalEntry_incomeStatement(item) -> dict:
    return {
        
        "date_entry": str(item["date_entry"]),
        
        "acoount_number": str(item["acoount_number"]),
        "account_disc": str(item["account_disc"]),
        "debit_amount": str(item["debit_amount"]),
        "credit_amount": str(item["credit_amount"]),
        
    }

def journalEntry_incomeStatements(entity) -> list:
    return [journalEntry_incomeStatement(item) for item in entity] 