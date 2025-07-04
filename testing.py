# Original code
def process_transactions(transactions):
    total = 0
    for transaction in transactions:
        if transaction['type'] == 'credit':
            total += transaction['amount']
        elif transaction['type'] == 'debit':
            total -= transaction['amount']
    return total
