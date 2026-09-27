from app.report import monthly_summary


def test_monthly_summary():
    result = monthly_summary(revenue=125000, expenses=98250.75)
    assert result["revenue"] == "$125,000.00"
    assert result["expenses"] == "$98,250.75"
    assert result["profit"] == "$26,749.25"
    assert result["margin"] == "21.4%"
