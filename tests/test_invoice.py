from app.invoice import generate_invoice_line, generate_invoice


def test_generate_invoice_line():
    assert generate_invoice_line("Widget", 1250.5, 3) == "Widget x3 - $3,751.50"


def test_generate_invoice():
    items = [("Widget", 1250.5, 3), ("Gadget", 89.99, 10)]
    result = generate_invoice(items)
    assert "$3,751.50" in result
    assert "$899.90" in result
    assert "TOTAL: $4,651.40" in result
