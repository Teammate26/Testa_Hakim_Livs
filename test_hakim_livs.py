import re
from playwright.sync_api import Page, expect
from dotenv import load_dotenv
import os

load_dotenv()

admin_username = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")


def test_admin_login(page: Page):
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", admin_username)
    page.fill("input[placeholder='Password']", admin_password)
    page.click("button:has-text('Logga in')")
    page.wait_for_load_state("networkidle")
