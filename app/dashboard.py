from formatting.old_format import format_currency


def kpi_card(label, value):
    return {"label": label, "display_value": format_currency(value)}


def build_dashboard(kpis):
    return [kpi_card(label, value) for label, value in kpis.items()]
