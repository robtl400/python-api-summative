"""
CLI Frontend for Inventory Management System
Allows users to interact with the Flask API through command line.
"""

import requests
from openfoodfacts_api import search_product_by_barcode, search_product_by_name

# Base URL for our Flask API
API_URL = "http://127.0.0.1:5000"


def display_menu():
    """Display the main menu options."""
    print("\n=== Inventory Management System ===")
    print("1. View all inventory items")
    print("2. View single item by ID")
    print("3. Add new item")
    print("4. Update item (price/quantity)")
    print("5. Delete item")
    print("6. Search OpenFoodFacts by barcode")
    print("7. Search OpenFoodFacts by name")
    print("8. Add item from OpenFoodFacts")
    print("9. Exit")
    print("===================================")


def view_all_items():
    """Fetch and display all inventory items."""
    try:
        response = requests.get(f"{API_URL}/inventory", timeout=5)
        data = response.json()

        if data['status'] == 1:
            items = data['items']
            if items:
                print("\n--- All Inventory Items ---")
                for item in items:
                    print(f"ID: {item['id']}")
                    print(f"  Name: {item['product_name']}")
                    print(f"  Brand: {item['brands']}")
                    print(f"  Barcode: {item['barcode']}")
                    print(f"  Quantity: {item['quantity']}")
                    print(f"  Price: ${item['price']:.2f}")
                    print("-" * 30)
            else:
                print("No items in inventory.")
        else:
            print(f"Error: {data.get('error', 'Unknown error')}")

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")


def view_single_item():
    """Fetch and display a single item by ID."""
    try:
        item_id = input("Enter item ID: ").strip()
        if not item_id.isdigit():
            print("Error: Please enter a valid numeric ID.")
            return

        response = requests.get(f"{API_URL}/inventory/{item_id}", timeout=5)
        data = response.json()

        if data['status'] == 1:
            item = data['product']
            print("\n--- Item Details ---")
            print(f"ID: {item['id']}")
            print(f"Name: {item['product_name']}")
            print(f"Brand: {item['brands']}")
            print(f"Barcode: {item['barcode']}")
            print(f"Ingredients: {item['ingredients_text']}")
            print(f"Quantity: {item['quantity']}")
            print(f"Price: ${item['price']:.2f}")
        else:
            print(f"Error: {data.get('error', 'Item not found')}")

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")


def add_item():
    """Add a new item to inventory."""
    try:
        print("\n--- Add New Item ---")
        product_name = input("Product name: ").strip()
        if not product_name:
            print("Error: Product name is required.")
            return

        brands = input("Brand: ").strip()
        barcode = input("Barcode: ").strip()
        ingredients = input("Ingredients: ").strip()

        quantity_str = input("Quantity: ").strip()
        try:
            quantity = int(quantity_str) if quantity_str else 0
        except ValueError:
            print("Error: Invalid quantity.")
            return

        price_str = input("Price: ").strip()
        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            print("Error: Invalid price.")
            return

        item_data = {
            "product_name": product_name,
            "brands": brands,
            "barcode": barcode,
            "ingredients_text": ingredients,
            "quantity": quantity,
            "price": price
        }

        response = requests.post(f"{API_URL}/inventory", json=item_data, timeout=5)
        data = response.json()

        if data['status'] == 1:
            print(f"Item added successfully with ID: {data['product']['id']}")
        else:
            print(f"Error: {data.get('error', 'Failed to add item')}")

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_item():
    """Update an existing item's price or quantity."""
    try:
        item_id = input("Enter item ID to update: ").strip()
        if not item_id.isdigit():
            print("Error: Please enter a valid numeric ID.")
            return

        print("What would you like to update?")
        print("1. Price")
        print("2. Quantity")
        print("3. Both")

        choice = input("Enter choice (1-3): ").strip()

        update_data = {}

        if choice in ['1', '3']:
            price_str = input("New price: ").strip()
            try:
                update_data['price'] = float(price_str)
            except ValueError:
                print("Error: Invalid price.")
                return

        if choice in ['2', '3']:
            quantity_str = input("New quantity: ").strip()
            try:
                update_data['quantity'] = int(quantity_str)
            except ValueError:
                print("Error: Invalid quantity.")
                return

        if not update_data:
            print("No updates specified.")
            return

        response = requests.patch(f"{API_URL}/inventory/{item_id}", json=update_data, timeout=5)
        data = response.json()

        if data['status'] == 1:
            print("Item updated successfully!")
            item = data['product']
            print(f"  Quantity: {item['quantity']}")
            print(f"  Price: ${item['price']:.2f}")
        else:
            print(f"Error: {data.get('error', 'Failed to update item')}")

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")


def delete_item():
    """Delete an item from inventory."""
    try:
        item_id = input("Enter item ID to delete: ").strip()
        if not item_id.isdigit():
            print("Error: Please enter a valid numeric ID.")
            return

        confirm = input(f"Are you sure you want to delete item {item_id}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Delete cancelled.")
            return

        response = requests.delete(f"{API_URL}/inventory/{item_id}", timeout=5)
        data = response.json()

        if data['status'] == 1:
            print(f"Item '{data['product']['product_name']}' deleted successfully!")
        else:
            print(f"Error: {data.get('error', 'Failed to delete item')}")

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")


def search_by_barcode():
    """Search OpenFoodFacts API by barcode."""
    barcode = input("Enter barcode: ").strip()
    if not barcode:
        print("Error: Barcode is required.")
        return

    print("Searching OpenFoodFacts...")
    result = search_product_by_barcode(barcode)

    if result['status'] == 1:
        product = result['product']
        print("\n--- Product Found ---")
        print(f"Name: {product['product_name']}")
        print(f"Brand: {product['brands']}")
        print(f"Barcode: {product['barcode']}")
        print(f"Ingredients: {product['ingredients_text'][:100]}..." if len(product.get('ingredients_text', '')) > 100 else f"Ingredients: {product.get('ingredients_text', 'N/A')}")
    else:
        print(f"Error: {result.get('error', 'Product not found')}")


def search_by_name():
    """Search OpenFoodFacts API by product name."""
    name = input("Enter product name: ").strip()
    if not name:
        print("Error: Product name is required.")
        return

    print("Searching OpenFoodFacts...")
    result = search_product_by_name(name)

    if result['status'] == 1:
        products = result['products']
        print(f"\n--- Found {len(products)} products ---")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['product_name']} ({product['brands']})")
            print(f"   Barcode: {product['barcode']}")
    else:
        print(f"Error: {result.get('error', 'No products found')}")


def add_from_openfoodfacts():
    """Add an item to inventory using data from OpenFoodFacts."""
    barcode = input("Enter barcode to fetch from OpenFoodFacts: ").strip()
    if not barcode:
        print("Error: Barcode is required.")
        return

    print("Fetching from OpenFoodFacts...")
    result = search_product_by_barcode(barcode)

    if result['status'] != 1:
        print(f"Error: {result.get('error', 'Product not found')}")
        return

    product = result['product']
    print(f"\nFound: {product['product_name']} ({product['brands']})")

    # Get quantity and price from user
    quantity_str = input("Enter quantity to add: ").strip()
    try:
        quantity = int(quantity_str) if quantity_str else 0
    except ValueError:
        print("Error: Invalid quantity.")
        return

    price_str = input("Enter price: ").strip()
    try:
        price = float(price_str) if price_str else 0.0
    except ValueError:
        print("Error: Invalid price.")
        return

    # Add to inventory
    item_data = {
        "product_name": product['product_name'],
        "brands": product['brands'],
        "barcode": product['barcode'],
        "ingredients_text": product['ingredients_text'],
        "quantity": quantity,
        "price": price
    }

    try:
        response = requests.post(f"{API_URL}/inventory", json=item_data, timeout=5)
        data = response.json()

        if data['status'] == 1:
            print(f"Item added successfully with ID: {data['product']['id']}")
        else:
            print(f"Error: {data.get('error', 'Failed to add item')}")

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    """Main function to run the CLI application."""
    print("Welcome to the Inventory Management System!")
    print("Make sure the Flask server is running (python app.py)")

    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            view_all_items()
        elif choice == '2':
            view_single_item()
        elif choice == '3':
            add_item()
        elif choice == '4':
            update_item()
        elif choice == '5':
            delete_item()
        elif choice == '6':
            search_by_barcode()
        elif choice == '7':
            search_by_name()
        elif choice == '8':
            add_from_openfoodfacts()
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == '__main__':
    main()
