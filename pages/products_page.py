class ProductsPage:
    def __init__(self,page):
        self.page = page
    
    def list_products(self):
        products = self.page.locator('.inventory_item')
        items = []
        count = products.count()
        for i in range(count):
            title = products.nth(i).locator('.inventory_item_name').inner_text()
            price = products.nth(i).locator('.inventory_item_price').inner_text()
            items.append({"title": title, "price": price})
        return items
    
    def add_first_to_cart(self):
        first_add_btn = self.page.locator('.inventory_item').nth(0).locator('button')
        first_add_btn.click()
        return self.page.locator('.shopping_cart_badge').inner_text()