"""
The replacement for formatting.old_format. Adds thousands separators and
consistent decimal rounding.
"""


def format_currency(amount):
    return f"${amount:,.2f}"


def format_percent(fraction):
    return f"{fraction * 100:.1f}%"
