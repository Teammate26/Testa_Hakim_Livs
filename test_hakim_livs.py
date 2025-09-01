import re
from playwright.sync_api import Page, expect

username = "hakim@livs.se"
password = "jagäradmin"


def test_admin_add_product(page: Page):
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", username)
    page.fill("input[placeholder='Password']", password)
    page.click("button:has-text('Logga in')")
    page.wait_for_load_state("networkidle")


def test_admin_delete_product(page: Page):
    pass
