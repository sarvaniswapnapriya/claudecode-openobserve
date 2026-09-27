from app.email_receipt import render_receipt_email


def test_render_receipt_email():
    email = render_receipt_email("Alex", 1999.5)
    assert "$1,999.50" in email
    assert "Hi Alex," in email
