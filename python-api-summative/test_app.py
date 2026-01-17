"""
Unit tests for the Inventory Management System
Tests API endpoints, CLI commands, and external API interactions.
"""

import pytest
from unittest.mock import patch, MagicMock
import json

from app import app, inventory
from openfoodfacts_api import search_product_by_barcode, search_product_by_name


# Flask API Tests

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset inventory before each test."""
    global inventory
    inventory.clear()
    inventory.extend([
        {
            "id": 1,
            "barcode": "123456",
            "product_name": "Test Product",
            "brands": "Test Brand",
            "ingredients_text": "Test ingredients",
            "quantity": 10,
            "price": 5.99
        }
    ])


# API Endpoint Tests

def test_get_all_items(client):
    """Test GET /inventory returns all items."""
    response = client.get('/inventory')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 1
    assert len(data['items']) == 1


def test_get_single_item(client):
    """Test GET /inventory/<id> returns single item."""
    response = client.get('/inventory/1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['product']['product_name'] == 'Test Product'


def test_add_item(client):
    """Test POST /inventory adds new item."""
    new_item = {
        "product_name": "New Product",
        "brands": "New Brand",
        "quantity": 20,
        "price": 9.99
    }

    response = client.post('/inventory', json=new_item)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['status'] == 1
    assert 'id' in data['product']


def test_update_item(client):
    """Test PATCH /inventory/<id> updates item."""
    update_data = {"price": 7.99, "quantity": 25}

    response = client.patch('/inventory/1', json=update_data)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['product']['price'] == 7.99
    assert data['product']['quantity'] == 25


def test_delete_item(client):
    """Test DELETE /inventory/<id> removes item."""
    response = client.delete('/inventory/1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 1


# External API Tests

@patch('openfoodfacts_api.requests.get')
def test_search_by_barcode(mock_get):
    """Test OpenFoodFacts barcode search."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mock Product",
            "brands": "Mock Brand",
            "ingredients_text": "Mock ingredients"
        }
    }
    mock_get.return_value = mock_response

    result = search_product_by_barcode("123456")

    assert result['status'] == 1
    assert result['product']['product_name'] == 'Mock Product'


@patch('openfoodfacts_api.requests.get')
def test_search_by_name(mock_get):
    """Test OpenFoodFacts name search."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [
            {"code": "123", "product_name": "Product 1", "brands": "Brand 1", "ingredients_text": ""}
        ]
    }
    mock_get.return_value = mock_response

    result = search_product_by_name("test")

    assert result['status'] == 1
    assert len(result['products']) == 1


# CLI Tests

@patch('cli.requests.get')
def test_cli_view_items(mock_get):
    """Test CLI view all items function."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "items": [{"id": 1, "product_name": "Test", "brands": "Brand",
                  "barcode": "123", "quantity": 10, "price": 5.99}]
    }
    mock_get.return_value = mock_response

    from cli import view_all_items
    view_all_items()

    mock_get.assert_called_once()


@patch('cli.requests.post')
@patch('builtins.input')
def test_cli_add_item(mock_input, mock_post):
    """Test CLI add item function."""
    mock_input.side_effect = ['New Product', 'Brand', '123', 'ingredients', '10', '5.99']
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 1, "product": {"id": 1, "product_name": "New Product"}}
    mock_post.return_value = mock_response

    from cli import add_item
    add_item()

    mock_post.assert_called_once()


@patch('cli.requests.delete')
@patch('builtins.input')
def test_cli_delete_item(mock_input, mock_delete):
    """Test CLI delete item function."""
    mock_input.side_effect = ['1', 'y']
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 1, "product": {"product_name": "Deleted"}}
    mock_delete.return_value = mock_response

    from cli import delete_item
    delete_item()

    mock_delete.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
