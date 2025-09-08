import re
from playwright.sync_api import Page, expect
from dotenv import load_dotenv
import os
from models.home import HomePage
from models.login import LoginPage
from models.cart import CartPage

load_dotenv()

user_username = os.getenv("USER1_USERNAME")
user_password = os.getenv("USER1_PASSWORD")
user_firstname = os.getenv("USER1_FIRSTNAME")

# Given I am a registered customer
# When I log in to the site using my valid credentials
# I should have access to my account


def test_user_login_and_verify_profile(page: Page):
    ### ARRANGE
    home_page = HomePage(page)
    login_page = LoginPage(page)

    ### ACT
    home_page.navigate()

    home_page.navigate_to_login()

    login_page.login_user(user_username, user_password)
    welcome_message = home_page.user_welcome

    ### ASSERT
    expect(welcome_message).to_have_text(user_firstname)
    page.wait_for_load_state("networkidle")


def test_user_reject_login_with_incorrect_password(page: Page):
    ### ARRANGE
    home_page = HomePage(page)
    login_page = LoginPage(page)

    ### ACT
    home_page.navigate()

    home_page.navigate_to_login()

    login_page.login_user(user_username, "pass1")

    error_message = login_page.login_error_message

    ### ASSERT

    expect(error_message).to_have_text("Inloggning misslyckades: Password is incorrect")
    page.wait_for_load_state("networkidle")


# # Given I am a logged in customer
# # When I add my chosen products
# # I should be able to view them and change quantity and amount on page and in my cart


def test_user_add_and_edit_products(page: Page):
    ### ARRANGE
    home_page = HomePage(page)
    login_page = LoginPage(page)
    cart_page = CartPage(page)

    ### ACT
    home_page.navigate()

    home_page.navigate_to_login()

    login_page.login_user(user_username, user_password)

    # Add 4 grönsakssoppa
    for product_additions in range(4):
        home_page.add_product_to_basket("Grönsakssoppa")

    # Add 4 Dinomatta
    for product_additions in range(4):
        home_page.add_product_to_basket("Dino Matta")

    # Add 2 Finkrossade tomater
    for product_additions in range(2):
        home_page.add_product_to_basket("Finkrossade tomater")

    # Remove 1 Dinomatta

    home_page.remove_product_from_basket("Dino Matta")

    # Go to Cart

    home_page.navigate_to_cart()

    # Add 1 Grönsakssoppa in cart
    cart_page.add_product_to_basket("Grönsakssoppa")

    # Remove 2 Grönsakssoppa in cart
    for product_additions in range(2):
        cart_page.remove_product_from_basket("Grönsakssoppa")

    # Remove all "Finkrossade Tomater" in cart
    cart_page.remove_all_products_from_basket("Finkrossade tomater")

    ### ASSERT
    ## Setup

    # Fetch first product quantity
    first_product_quantity = cart_page.fetch_existing_product_quantity("Grönsakssoppa")

    # Fetch second product quantity
    second_product_quantity = cart_page.fetch_existing_product_quantity("Dino Matta")

    ## Assertions
    # Assert quantity of remaining products
    expect(first_product_quantity).to_have_text(f"x{3}")
    expect(second_product_quantity).to_have_text(f"x{3}")

    # Assert removed product is no longer in cart
    removed_product = cart_page.fetch_existing_product("Finkrossade tomater")
    expect(removed_product).to_have_count(0)
    page.wait_for_load_state("networkidle")
