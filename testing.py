def process_transactions(transactions):
    total = 0
    for transaction in transactions:
        amount = transaction.get('amount', 0)
        if transaction.get('type') == 'credit':
            total += amount
        elif transaction.get('type') == 'debit':
            total -= amount
    return total
