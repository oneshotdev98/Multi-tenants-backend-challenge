def score_match(invoice, tx):
    score = 0

    if invoice.amount == tx.amount:
        score += 50
    elif abs(invoice.amount - tx.amount) <= 5:
        score += 20

    if invoice.invoice_date and tx.posted_at:
        if abs((invoice.invoice_date - tx.posted_at).days) <= 3:
            score += 20

    if invoice.description and tx.description:
        if invoice.description.lower() in tx.description.lower():
            score += 10

    return score