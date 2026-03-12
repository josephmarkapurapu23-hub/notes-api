import sys , os
from typing import Any
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
import openpyxl # type: ignore

def test_login_and_add_to_cart(page: Any):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(page)
    items = products.list_products()
    print("products:")
    for i ,item in enumerate(items):
         print(f"{i+1}. {item['title']} — {item['price']}")

    badge = products.add_first_to_cart()
    assert badge == "1" , "cart badge didnot update!"
    print("Cart badge after add:", badge)

    excel_path = r'E:\python\notes-api\test_output.xlsx'

    wb = openpyxl.Workbook() # type: ignore
    ws = wb.active
    ws.title = "products"

    ws.append(["S.no", "Prodcut Name", "Price"])

    for i, item in enumerate(items):
         ws.append([i+1, item['title'], item['price']])

         ws.append([])
         ws.append(['cart badge after add', badge])

         wb.save(excel_path)
         print(f"results saved to {excel_path}")


    