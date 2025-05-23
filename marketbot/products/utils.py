# products/utils.py
from products.models import Product


def save_products_from_json(json_data):
    items = json_data.get("items", [])
    for item in items:
        product, created = Product.objects.update_or_create(
            productId=item["productId"],
            defaults={
                "brand": item.get("brand", ""),
                "maker": item.get("maker", ""),
                "title": item.get("title", ""),
                "image": item.get("image", ""),
                "link": item.get("link", ""),
                "lprice": item.get("lprice", ""),
                "hprice": item.get("hprice", ""),
                "mallName": item.get("mallName", ""),
                "productType": item.get("productType", ""),
                "category1": item.get("category1", ""),
                "category2": item.get("category2", ""),
                "category3": item.get("category3", ""),
                "category4": item.get("category4", ""),
            }
        )
