from formatting.old_format import format_currency


def render_receipt_email(customer_name, amount_paid):
    return (
        f"Hi {customer_name},\n\n"
        f"We've received your payment of {format_currency(amount_paid)}. "
        f"Thank you for your business."
    )
