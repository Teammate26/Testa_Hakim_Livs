class CartPage:
    def __init__(self, page):
        self.page = page
        self.fetch_product = page.locator("div.cart-table-container td")

    def add_product_to_basket(self, product):
        product_item = self.fetch_product.filter(has_text=product)
        add_button = product_item.locator("button", has_text="+1")
        add_button.click()

    def remove_product_from_basket(self, product):
        product_item = self.fetch_product.filter(has_text=product)
        remove_button = product_item.locator("button", has_text="-1")
        remove_button.click()

    def remove_all_products_from_basket(self, product):
        product_item = self.fetch_product.filter(has_text=product)
        remove_button = product_item.locator("button", has_text="Ta bort alla")
        remove_button.click()

    def fetch_existing_product(self, product):
        return self.fetch_product.filter(has_text=product)

    def fetch_existing_product_quantity(self, product):
        product_item = self.fetch_product.filter(has_text=product)
        product_quantity = product_item.locator("span.quantity")
        return product_quantity
