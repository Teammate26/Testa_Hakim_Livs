class HomePage:
    def __init__(self, page):
        self.page = page
        self.go_to_login_btn = page.locator("#login-li")
        self.user_welcome = page.locator("div.dropdown-trigger")
        self.fetch_product = self.page.locator("#products .product-card")
        self.go_to_cart = page.locator("a.cart-link")

    def navigate(self):
        self.page.goto("https://webshop-2025-fe-g1-one.vercel.app/")

    def navigate_to_login(self):
        self.go_to_login_btn.click()

    def add_product_to_basket(self, product):
        product_item = self.fetch_product.filter(has_text=product)
        add_button = product_item.locator("button.add-to-cart-btn")
        add_button.click()

    def remove_product_from_basket(self, product):
        product_item = self.fetch_product.filter(has_text=product)
        remove_button = product_item.locator("button.remove-from-cart-btn")
        remove_button.click()

    def navigate_to_cart(self):
        self.go_to_cart.click()
