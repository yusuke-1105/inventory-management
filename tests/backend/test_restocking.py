"""
Tests for restocking order API endpoints.
"""
import pytest


class TestRestockingEndpoints:
    """Test suite for restocking-related endpoints."""

    def test_demand_forecast_includes_restocking_fields(self, client):
        """Test that demand forecasts now expose unit_cost and lead_time_days."""
        response = client.get("/api/demand")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "unit_cost" in item
            assert "lead_time_days" in item
            assert isinstance(item["unit_cost"], (int, float))
            assert isinstance(item["lead_time_days"], int)
            assert item["unit_cost"] > 0
            assert item["lead_time_days"] > 0

    def test_get_restocking_orders_returns_list(self, client):
        """Test that the restocking orders list endpoint returns a list."""
        response = client.get("/api/restocking/orders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_restocking_order_success(self, client):
        """Test submitting a valid restocking order."""
        payload = {
            "budget": 1000,
            "items": [
                {
                    "sku": "WDG-001",
                    "name": "Industrial Widget Type A",
                    "quantity": 10,
                    "unit_cost": 12.5,
                    "lead_time_days": 10
                },
                {
                    "sku": "GSK-203",
                    "name": "High-Temperature Gasket",
                    "quantity": 5,
                    "unit_cost": 4.2,
                    "lead_time_days": 5
                }
            ]
        }

        response = client.post("/api/restocking/orders", json=payload)
        assert response.status_code == 201

        data = response.json()
        assert "id" in data
        assert data["order_number"].startswith("RESTOCK-")

        # total_cost = 10*12.5 + 5*4.2 = 146.0
        assert abs(data["total_cost"] - 146.0) < 0.01

        # lead_time_days is the MAX across items, not sum/average
        assert data["lead_time_days"] == 10

        assert data["status"] == "Submitted"
        assert data["budget"] == 1000

        # created_date/expected_delivery are ISO datetimes
        assert "T" in data["created_date"]
        assert "T" in data["expected_delivery"]

    def test_create_restocking_order_empty_items_returns_400(self, client):
        """Test that submitting an order with no items is rejected."""
        response = client.post("/api/restocking/orders", json={"budget": 500, "items": []})
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data

    def test_created_order_appears_in_subsequent_get(self, client):
        """Test that a submitted order is persisted in-memory and returned by GET."""
        before = client.get("/api/restocking/orders").json()
        before_count = len(before)

        payload = {
            "budget": 200,
            "items": [
                {
                    "sku": "FLT-405",
                    "name": "Oil Filter Cartridge",
                    "quantity": 20,
                    "unit_cost": 3.15,
                    "lead_time_days": 4
                }
            ]
        }
        create_response = client.post("/api/restocking/orders", json=payload)
        assert create_response.status_code == 201
        created_order = create_response.json()

        after = client.get("/api/restocking/orders").json()
        assert len(after) == before_count + 1
        assert any(o["id"] == created_order["id"] for o in after)

    def test_restocking_order_expected_delivery_matches_lead_time(self, client):
        """Test that expected_delivery is created_date + lead_time_days."""
        from datetime import datetime

        payload = {
            "budget": 500,
            "items": [
                {
                    "sku": "VLV-506",
                    "name": "Pressure Relief Valve",
                    "quantity": 3,
                    "unit_cost": 22.6,
                    "lead_time_days": 12
                }
            ]
        }
        response = client.post("/api/restocking/orders", json=payload)
        assert response.status_code == 201

        data = response.json()
        created = datetime.fromisoformat(data["created_date"])
        expected = datetime.fromisoformat(data["expected_delivery"])
        assert (expected - created).days == 12
