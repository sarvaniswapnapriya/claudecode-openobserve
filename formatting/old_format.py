"""
DEPRECATED. Do not import from this module in new code.

format_currency() here is the old implementation: it does no thousands
separator and no decimal rounding, which produces inconsistent output like
"$1234.5" or "$1000000". Use formatting.new_format instead.
"""


def format_currency(amount):
    return f"${amount}"


def format_percent(fraction):
    return f"{fraction * 100}%"
