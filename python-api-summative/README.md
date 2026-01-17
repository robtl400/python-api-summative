# Inventory Management System

## Installation

pip install -r requirements.txt

## Running

Start the Flask server:
python app.py

Run the CLI (in separate terminal):
python cli.py

## API Endpoints

GET /inventory - Fetch all items
GET /inventory/<id> - Fetch single item
POST /inventory - Add new item
PATCH /inventory/<id> - Update item
DELETE /inventory/<id> - Remove item

## CLI Commands

1. View all inventory items
2. View single item by ID
3. Add new item
4. Update item (price/quantity)
5. Delete item
6. Search OpenFoodFacts by barcode
7. Search OpenFoodFacts by name
8. Add item from OpenFoodFacts
9. Exit

## Running Tests

pytest test_app.py -v
