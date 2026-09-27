from formatting.old_format import format_currency


def generate_invoice_line(item_name, unit_price, quantity):
    total = unit_price * quantity
    return f"{item_name} x{quantity} - {format_currency(total)}"


def generate_invoice(items):
    lines = [generate_invoice_line(name, price, qty) for name, price, qty in items]
    grand_total = sum(price * qty for _, price, qty in items)
    lines.append(f"TOTAL: {format_currency(grand_total)}")
    return "\n".join(lines)
