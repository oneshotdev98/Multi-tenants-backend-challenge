def test_import_transactions_and_idempotency_replay(client):
    tenant_resp = client.post("/tenants", json={"name": "Tags"})
    tenant_id = tenant_resp.json()["id"]

    payload = [
        {
            "external_id": "tx-100",
            "amount": 100,
            "currency": "USD",
            "description": "Office Supplies Payment",
            "posted_at": "2026-02-21T00:00:00",
        }
    ]

    first = client.post(
        f"/tenants/{tenant_id}/bank-transactions/import",
        headers={"Idempotency-Key": "idem-1"},
        json=payload,
    )
    assert first.status_code == 200
    first_data = first.json()
    assert len(first_data) == 1
    assert first_data[0]["tenant_id"] == tenant_id
    assert first_data[0]["id"]
    assert first_data[0]["created_at"]

    replay = client.post(
        f"/tenants/{tenant_id}/bank-transactions/import",
        headers={"Idempotency-Key": "idem-1"},
        json=payload,
    )
    assert replay.status_code == 200
    assert replay.json() == first_data


def test_import_transactions_idempotency_conflict(client):
    tenant_resp = client.post("/tenants", json={"name": "Tags"})
    tenant_id = tenant_resp.json()["id"]

    first_payload = [
        {
            "external_id": "tx-101",
            "amount": 100,
            "currency": "USD",
            "description": "Payment A",
            "posted_at": "2026-02-21T00:00:00",
        }
    ]
    second_payload = [
        {
            "external_id": "tx-102",
            "amount": 200,
            "currency": "USD",
            "description": "Payment B",
            "posted_at": "2026-02-22T00:00:00",
        }
    ]

    first = client.post(
        f"/tenants/{tenant_id}/bank-transactions/import",
        headers={"Idempotency-Key": "idem-2"},
        json=first_payload,
    )
    assert first.status_code == 200

    conflict = client.post(
        f"/tenants/{tenant_id}/bank-transactions/import",
        headers={"Idempotency-Key": "idem-2"},
        json=second_payload,
    )
    assert conflict.status_code == 409
