"""
Flask REST API for Inventory Management System
Provides CRUD operations for managing inventory items.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database - array to store inventory items
# Each item contains an ID and product information similar to OpenFoodFacts structure
inventory = [
    {
        "id": 1,
        "barcode": "0041570054529",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "quantity": 50,
        "price": 4.99
    },
    {
        "id": 2,
        "barcode": "0011110038364",
        "product_name": "Whole Grain Bread",
        "brands": "Nature's Own",
        "ingredients_text": "Whole wheat flour, water, sugar, yeast, salt",
        "quantity": 30,
        "price": 3.49
    },
    {
        "id": 3,
        "barcode": "0028400064057",
        "product_name": "Potato Chips",
        "brands": "Lay's",
        "ingredients_text": "Potatoes, vegetable oil, salt",
        "quantity": 100,
        "price": 2.99
    }
]

# Counter for generating unique IDs
next_id = 4


@app.route('/inventory', methods=['GET'])
def get_all_items():
    """Fetch all inventory items."""
    return jsonify({"status": 1, "items": inventory})


@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Fetch a single inventory item by ID."""
    for item in inventory:
        if item['id'] == item_id:
            return jsonify({"status": 1, "product": item})
    return jsonify({"status": 0, "error": "Item not found"}), 404


@app.route('/inventory', methods=['POST'])
def add_item():
    """Add a new inventory item."""
    global next_id

    data = request.get_json()

    # Validate required fields
    if not data or 'product_name' not in data:
        return jsonify({"status": 0, "error": "Product name is required"}), 400

    # Create new item with auto-generated ID
    new_item = {
        "id": next_id,
        "barcode": data.get('barcode', ''),
        "product_name": data.get('product_name', ''),
        "brands": data.get('brands', ''),
        "ingredients_text": data.get('ingredients_text', ''),
        "quantity": data.get('quantity', 0),
        "price": data.get('price', 0.0)
    }

    inventory.append(new_item)
    next_id += 1

    return jsonify({"status": 1, "product": new_item}), 201


@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    """Update an existing inventory item."""
    data = request.get_json()

    if not data or len(data) == 0:
        return jsonify({"status": 0, "error": "No data provided"}), 400

    for item in inventory:
        if item['id'] == item_id:
            # Update only the fields that are provided
            if 'product_name' in data:
                item['product_name'] = data['product_name']
            if 'brands' in data:
                item['brands'] = data['brands']
            if 'barcode' in data:
                item['barcode'] = data['barcode']
            if 'ingredients_text' in data:
                item['ingredients_text'] = data['ingredients_text']
            if 'quantity' in data:
                item['quantity'] = data['quantity']
            if 'price' in data:
                item['price'] = data['price']

            return jsonify({"status": 1, "product": item})

    return jsonify({"status": 0, "error": "Item not found"}), 404


@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Remove an inventory item."""
    for i, item in enumerate(inventory):
        if item['id'] == item_id:
            deleted_item = inventory.pop(i)
            return jsonify({"status": 1, "message": "Item deleted", "product": deleted_item})

    return jsonify({"status": 0, "error": "Item not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
