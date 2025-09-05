class LoginPage:
    def __init__(self, page):
        self.page = page
        self.register_prompt_header = page.get_by_text("Ny hos Hakim Livs?")
        self.go_to_register_btn = page.locator("#createAccountBtn")
        self.input_username = page.locator("#username")
        self.input_password = page.locator("#password")
        self.button_login = page.locator("#loginBtn")
        self.login_error_message = page.locator("div.error-message.showElement")

    def login_user(self, username, password):
        self.input_username.fill(username)
        self.input_password.fill(password)
        self.button_login.click()
