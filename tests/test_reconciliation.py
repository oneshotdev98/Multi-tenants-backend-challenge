def _setup_invoice_and_transaction(client):
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
    assert invoice_resp.status_code == 200

    tx_resp = client.post(
        f"/tenants/{tenant_id}/bank-transactions/import",
        headers={"Idempotency-Key": "reconcile-seed"},
        json=[
            {
                "external_id": "tx-200",
                "amount": 100,
                "currency": "USD",
                "description": "Office Supplies Payment",
                "posted_at": "2026-02-21T00:00:00",
            }
        ],
    )
    assert tx_resp.status_code == 200

    return tenant_id


def test_reconcile_returns_proposed_match(client):
    tenant_id = _setup_invoice_and_transaction(client)

    resp = client.post(f"/tenants/{tenant_id}/reconcile")
    assert resp.status_code == 200

    matches = resp.json()
    assert len(matches) >= 1

    match = matches[0]
    assert match["id"]
    assert match["tenant_id"] == tenant_id
    assert match["status"] == "proposed"
    assert match["created_at"]
    assert match["score"] > 0


def test_reconcile_requires_transactions(client):
    tenant_resp = client.post("/tenants", json={"name": "Tags"})
    tenant_id = tenant_resp.json()["id"]

    client.post(
        f"/tenants/{tenant_id}/invoices",
        json={"amount": 100, "description": "Office Supplies"},
    )

    resp = client.post(f"/tenants/{tenant_id}/reconcile")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "No bank transactions found for tenant"
