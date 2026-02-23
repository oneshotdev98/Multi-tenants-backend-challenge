def test_ai_explain_endpoint_returns_text(client):
    tenant_resp = client.post("/tenants", json={"name": "Tags"})
    tenant_id = tenant_resp.json()["id"]

    invoice_resp = client.post(
        f"/tenants/{tenant_id}/invoices",
        json={
            "amount": 100,
            "currency": "USD",
            "description": "Office Supplies",
            "invoice_date": "2026-02-20T00:00:00",
        },
    )
    invoice_id = invoice_resp.json()["id"]

    tx_resp = client.post(
        f"/tenants/{tenant_id}/bank-transactions/import",
        headers={"Idempotency-Key": "ai-seed"},
        json=[
            {
                "external_id": "tx-400",
                "amount": 100,
                "currency": "USD",
                "description": "Office Supplies Payment",
                "posted_at": "2026-02-21T00:00:00",
            }
        ],
    )
    tx_id = tx_resp.json()[0]["id"]

    explain_resp = client.get(
        f"/tenants/{tenant_id}/reconcile/explain",
        params={"invoice_id": invoice_id, "transaction_id": tx_id},
    )

    assert explain_resp.status_code == 200
    body = explain_resp.json()
    assert isinstance(body.get("explanation"), str)
    assert body["explanation"].strip()
