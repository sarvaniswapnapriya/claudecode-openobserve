from app.dashboard import kpi_card, build_dashboard


def test_kpi_card():
    result = kpi_card("Monthly Revenue", 42500)
    assert result["display_value"] == "$42,500.00"


def test_build_dashboard():
    kpis = {"Revenue": 1000000, "Costs": 250000.5}
    result = build_dashboard(kpis)
    values = {item["label"]: item["display_value"] for item in result}
    assert values["Revenue"] == "$1,000,000.00"
    assert values["Costs"] == "$250,000.50"
