from formatting.old_format import format_currency, format_percent


def monthly_summary(revenue, expenses):
    profit = revenue - expenses
    margin = profit / revenue if revenue else 0
    return {
        "revenue": format_currency(revenue),
        "expenses": format_currency(expenses),
        "profit": format_currency(profit),
        "margin": format_percent(margin),
    }
