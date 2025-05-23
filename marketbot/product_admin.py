# product_admin.py
import django
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketbot.settings")
django.setup()

from products.models import Product

def list_products():
    for p in Product.objects.all():
        print(f"{p.productId} | {p.title} | {p.lprice}")

def add_product():
    data = {
        "productId": input("productId: "),
        "brand": input("brand: "),
        "maker": input("maker: "),
        "title": input("title: "),
        "image": input("image: "),
        "link": input("link: "),
        "lprice": input("lprice: "),
        "hprice": input("hprice: "),
        "mallName": input("mallName: "),
        "productType": input("productType: "),
        "category1": input("category1: "),
        "category2": input("category2: "),
        "category3": input("category3: "),
        "category4": input("category4: "),
    }
    Product.objects.update_or_create(productId=data["productId"], defaults=data)
    print("저장 완료!")

def edit_product():
    pid = input("수정할 productId 입력: ")
    try:
        product = Product.objects.get(productId=pid)
    except Product.DoesNotExist:
        print(" 해당 productId의 상품이 존재하지 않습니다.")
        return

    print(f"현재 이름: {product.title}")
    new_title = input("새로운 title (그대로 두려면 Enter): ")
    if new_title:
        product.title = new_title

    new_price = input(f"현재 lprice: {product.lprice} → 새 lprice (그대로 두려면 Enter): ")
    if new_price:
        product.lprice = new_price

    product.save()
    print(" 수정 완료!")

def main():
    while True:
        cmd = input("\n1) 목록  2) 추가  3) 삭제  4) 수정  0) 종료\n>>> ")
        if cmd == "1":
            list_products()
        elif cmd == "2":
            add_product()
        elif cmd == "3":
            delete_product()
        elif cmd == "4":
            edit_product()
        elif cmd == "0":
            break

if __name__ == "__main__":
    main()
