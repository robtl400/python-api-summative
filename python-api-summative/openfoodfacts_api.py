"""
OpenFoodFacts API Integration Module
Fetches product details from the OpenFoodFacts external API.
"""

import requests

# Base URL for OpenFoodFacts API
BASE_URL = "https://world.openfoodfacts.org/api/v2"


def search_product_by_barcode(barcode):
    """
    Fetch product details from OpenFoodFacts API using a barcode.

    Args:
        barcode: The product barcode to search for

    Returns:
        Dictionary with product data or error information
    """
    try:
        url = f"{BASE_URL}/product/{barcode}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                product = data.get('product', {})
                return {
                    "status": 1,
                    "product": {
                        "barcode": barcode,
                        "product_name": product.get('product_name', 'Unknown'),
                        "brands": product.get('brands', 'Unknown'),
                        "ingredients_text": product.get('ingredients_text', ''),
                        "categories": product.get('categories', ''),
                        "image_url": product.get('image_url', '')
                    }
                }
            else:
                return {"status": 0, "error": "Product not found"}
        else:
            return {"status": 0, "error": f"API error: {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"status": 0, "error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"status": 0, "error": f"Request failed: {str(e)}"}


def search_product_by_name(name):
    """
    Search for products by name on OpenFoodFacts API.

    Args:
        name: The product name to search for

    Returns:
        Dictionary with list of matching products or error information
    """
    try:
        url = f"{BASE_URL}/search"
        params = {
            "search_terms": name,
            "page_size": 5,
            "fields": "code,product_name,brands,ingredients_text"
        }
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])

            if products:
                result_list = []
                for p in products:
                    result_list.append({
                        "barcode": p.get('code', ''),
                        "product_name": p.get('product_name', 'Unknown'),
                        "brands": p.get('brands', 'Unknown'),
                        "ingredients_text": p.get('ingredients_text', '')
                    })
                return {"status": 1, "products": result_list}
            else:
                return {"status": 0, "error": "No products found"}
        else:
            return {"status": 0, "error": f"API error: {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"status": 0, "error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"status": 0, "error": f"Request failed: {str(e)}"}
