from billing_engine import build_billing_summary


def generate_invoices():
    billing = build_billing_summary()

    invoices = []

    for account in billing:

        invoices.append({
            "api_key": account["api_key"],
            "plan": account["plan"],
            "usage_count": account["usage_count"],
            "amount_due": account["monthly_price"],
            "currency": "USD",
            "invoice_status": "pending"
        })

    return invoices
