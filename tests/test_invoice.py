def test_create_invoice(client):
    tenant_resp = client.post("/tenants", json={"name": "A"})
    assert tenant_resp.status_code == 200
    tenant = tenant_resp.json()

    invoice_resp = client.post(
        f"/tenants/{tenant['id']}/invoices",
        json={"amount": 100, "currency": "USD", "description": "Office Supplies"},
    )
    assert invoice_resp.status_code == 200

    invoice = invoice_resp.json()
    assert invoice["tenant_id"] == tenant["id"]
    assert invoice["status"] == "open"
    assert invoice["id"]
