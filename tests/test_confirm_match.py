def _seed_match(client):
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

    client.post(
        f"/tenants/{tenant_id}/bank-transactions/import",
        headers={"Idempotency-Key": "confirm-seed"},
        json=[
            {
                "external_id": "tx-300",
                "amount": 100,
                "currency": "USD",
                "description": "Office Supplies Payment",
                "posted_at": "2026-02-21T00:00:00",
            }
        ],
    )

    reconcile_resp = client.post(f"/tenants/{tenant_id}/reconcile")
    match_id = reconcile_resp.json()[0]["id"]

    return tenant_id, match_id, invoice_id


def test_confirm_match_updates_match_and_invoice(client):
    tenant_id, match_id, invoice_id = _seed_match(client)

    confirm_resp = client.post(f"/tenants/{tenant_id}/matches/{match_id}/confirm")
    assert confirm_resp.status_code == 200
    assert confirm_resp.json()["status"] == "confirmed"

    invoices_resp = client.get(f"/tenants/{tenant_id}/invoices")
    assert invoices_resp.status_code == 200
    invoices = invoices_resp.json()

    target = next(inv for inv in invoices if inv["id"] == invoice_id)
    assert target["status"] == "matched"


def test_confirm_match_twice_returns_conflict(client):
    tenant_id, match_id, _ = _seed_match(client)

    first = client.post(f"/tenants/{tenant_id}/matches/{match_id}/confirm")
    assert first.status_code == 200

    second = client.post(f"/tenants/{tenant_id}/matches/{match_id}/confirm")
    assert second.status_code == 409
