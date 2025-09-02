import re
from playwright.sync_api import Page, expect
from dotenv import load_dotenv
import os

load_dotenv()

user_username = os.getenv("USER1_USERNAME")
user_password = os.getenv("USER1_PASSWORD")
user_firstname = os.getenv("USER1_FIRSTNAME")

# Given I am a registered customer
# When I log in to the site using my valid credentials
# I should have access to my account


def test_user_login_and_verify_profile(page: Page):
    ### ACT
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", user_username)
    page.fill("input[placeholder='Password']", user_password)
    page.click("button:has-text('Logga in')")
    user_welcome = page.locator("div.dropdown-trigger")

    ### ASSERT
    expect(user_welcome).to_have_text(user_firstname)
    page.wait_for_load_state("networkidle")


def test_user_reject_login_with_incorrect_password(page: Page):
    ### ACT
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", user_username)
    page.fill("input[placeholder='Password']", "pass1")
    page.click("button:has-text('Logga in')")

    ### ASSERT
    error_message = page.locator("div.error-message.showElement")
    expect(error_message).to_have_text("Inloggning misslyckades: Password is incorrect")
    page.wait_for_load_state("networkidle")


# Given I am a logged in customer
# When I add my chosen products
# I should be able to view them and change quantity and amount on page and in my cart


def test_user_add_and_edit_products(page: Page):
    ### ACT
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", user_username)
    page.fill("input[placeholder='Password']", user_password)
    page.click("button:has-text('Logga in')")

    # Add 4 grönsakssoppa
    page.locator("#products .product-card").filter(has_text="Grönsakssoppa").locator(
        "button.add-to-cart-btn"
    ).click()
    page.locator("#products .product-card").filter(has_text="Grönsakssoppa").locator(
        "button.add-to-cart-btn"
    ).click()
    page.locator("#products .product-card").filter(has_text="Grönsakssoppa").locator(
        "button.add-to-cart-btn"
    ).click()
    page.locator("#products .product-card").filter(has_text="Grönsakssoppa").locator(
        "button.add-to-cart-btn"
    ).click()

    # Add 4 Dinomatta
    page.locator("#products .product-card").filter(has_text="Dino Matta").locator(
        "button.add-to-cart-btn"
    ).click()
    page.locator("#products .product-card").filter(has_text="Dino Matta").locator(
        "button.add-to-cart-btn"
    ).click()
    page.locator("#products .product-card").filter(has_text="Dino Matta").locator(
        "button.add-to-cart-btn"
    ).click()
    page.locator("#products .product-card").filter(has_text="Dino Matta").locator(
        "button.add-to-cart-btn"
    ).click()

    # Add 2 Finkrossade tomater

    page.locator("#products .product-card").filter(
        has_text="Finkrossade tomater"
    ).locator("button.add-to-cart-btn").click()
    page.locator("#products .product-card").filter(
        has_text="Finkrossade tomater"
    ).locator("button.add-to-cart-btn").click()

    # Remove 1 Dinomatta

    page.locator("#products .product-card").filter(has_text="Dino Matta").locator(
        "button.remove-from-cart-btn"
    ).click()

    # Go to Cart

    page.locator("a.cart-link").click()

    # Remove 1 Grönsakssoppa in cart
    page.locator("div.cart-table-container td").filter(
        has_text="Grönsakssoppa"
    ).locator("button", has_text="-1").click()

    # Remove all "Finkrossade Tomater" in cart
    page.locator("div.cart-table-container td").filter(
        has_text="Finkrossade Tomater"
    ).locator("button", has_text="Ta bort alla").click()

    ### ASSERT
    ## Setup
    # Fetch overarching product container
    cart_container = page.locator("div.cart-table-container")

    # Fetch first product quantity
    first_product = cart_container.locator("td").filter(has_text="Grönsakssoppa")
    first_product_quantity = first_product.locator("span.quantity")

    # Fetch second product quantity
    second_product = cart_container.locator("td").filter(has_text="Dino Matta")
    second_product_quantity = second_product.locator("span.quantity")

    ## Assertions
    # Assert quantity of remaining products
    expect(first_product_quantity).to_have_text(f"x{3}")
    expect(second_product_quantity).to_have_text(f"x{3}")

    # Assert removed product is no longer in cart
    removed_product = cart_container.locator("td").filter(
        has_text="Finkrossade Tomater"
    )
    expect(removed_product).to_have_count(0)
    page.wait_for_load_state("networkidle")
