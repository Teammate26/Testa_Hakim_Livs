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

def test_admin_swap_price(page: Page):
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", admin_username)
    page.fill("input[placeholder='Password']", admin_password)
    page.click("button:has-text('Logga in')")
    page.wait_for_load_state("networkidle")

    page.hover("div.dropdown-trigger")
    page.wait_for_load_state("networkidle")
    page.click("div.dropdown-menu:has-text('Admin panel')")
    page.wait_for_load_state("networkidle")

    page.locator('button.update-btn[data-id="67efa09c2fb3b7701d73b8da"]').click()
    page.wait_for_load_state("networkidle")

    page.click("input#productPrice")
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type("15.95")

    page.click("button.save-btn:has-text('Spara produkt')")
    page.wait_for_load_state("networkidle")

    page.on("dialog", lambda dialog: dialog.accept())
    page.wait_for_load_state("networkidle")

    page.locator('button.update-btn[data-id="67efa09c2fb3b7701d73b8da"]').click()
    price_input = page.locator("input#productPrice")
    price_input.wait_for(state="visible")
    current_price = price_input.input_value()
    assert current_price == "15.95", f"Expected price should have been 15,95kr, but was {current_price}"

def test_admin_add_product(page: Page):
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", admin_username)
    page.fill("input[placeholder='Password']", admin_password)
    page.click("button:has-text('Logga in')")
    page.wait_for_load_state("networkidle")

    page.hover("div.dropdown-trigger")
    page.wait_for_load_state("networkidle")
    page.click("div.dropdown-menu:has-text('Admin panel')")
    page.wait_for_load_state("networkidle")
    page.click("button[id='addProductBtn']")
    page.fill("input[placeholder='Välj Image URL']", "https://evermade-raisio-multisite-website.s3.eu-north-1.amazonaws.com/wp-content/uploads/sites/6/2021/05/14135603/kalaspuffar_historien_006.png")
    page.fill("input[placeholder='Ange produktnamn']", "Saras kalaspuffar")

    page.click("input#productPrice")
    page.keyboard.type("19.95")
    page.locator("select#productUnit").select_option("g")

    page.fill("input[placeholder='Ange mängd av enhet']", "500")
    page.fill("input[placeholder='Ange produktens tillverkare']", "Hola bandola AB")
    page.fill("textarea[placeholder='Ange produktbeskrivning']", "Saras utmärkta kalaspuffar, ett helt halvt kilo direkt från våra fabriker hos Hola Bandola AB, adress Holabandolavägen 125, 893 32, Spanien")
    page.locator("select#productCategory").select_option("Skafferi")
    page.fill("input[placeholder='Ange lagersaldo']", "1000")

    page.click("button.save-btn")
    page.wait_for_load_state("networkidle")

    new_product = page.locator("td:has-text('Saras kalaspuffar')")
    expect(new_product).to_have_text("Saras kalaspuffar")

def test_admin_delete_product(page: Page):
    page.goto("https://webshop-2025-fe-g1-one.vercel.app/", wait_until="networkidle")

    expect(page.get_by_text("Alla produkter")).to_be_visible()
    page.click("a:has-text('Logga in')")

    page.fill("input[placeholder='E-postadress']", admin_username)
    page.fill("input[placeholder='Password']", admin_password)
    page.click("button:has-text('Logga in')")
    page.wait_for_load_state("networkidle")

    page.hover("div.dropdown-trigger")
    page.wait_for_load_state("networkidle")
    page.click("div.dropdown-menu:has-text('Admin panel')")
    page.wait_for_load_state("networkidle")
    page.click("button[id='addProductBtn']")
    page.fill("input[placeholder='Välj Image URL']", "https://1.bp.blogspot.com/-9St7jv207Fg/VDPmClWxHdI/AAAAAAAAUVg/MWWBHOfg5KY/s1600/Kalaspuffar,%2BHoney%2Bmonster%2Bfoods.JPG")
    page.fill("input[placeholder='Ange produktnamn']", "Saras extremt goda kalaspuffar")

    page.click("input#productPrice")
    page.keyboard.type("21.95")
    page.locator("select#productUnit").select_option("g")

    page.fill("input[placeholder='Ange mängd av enhet']", "400")
    page.fill("input[placeholder='Ange produktens tillverkare']", "Hola bandola AB")
    page.fill("textarea[placeholder='Ange produktbeskrivning']", "Saras extremt utmärkt goda kalaspuffar - men ät inom en timma så de inte blir dåliga (OBS kort hållbarhet). Nästan ett helt halvt kilo direkt från våra fabriker hos Hola Bandola AB, adress Holabandolavägen 125, 893 32, Spanien")
    page.locator("select#productCategory").select_option("Skafferi")
    page.fill("input[placeholder='Ange lagersaldo']", "300")

    page.click("button.save-btn")
    page.wait_for_load_state("networkidle")

    new_product = page.locator("td:has-text('Saras extremt goda kalaspuffar')")
    expect(new_product).to_have_text("Saras extremt goda kalaspuffar")

    page.wait_for_load_state("networkidle")

    page.once("dialog", lambda dialog: dialog.accept())
    page.locator('button.delete-btn[data-name="Saras extremt goda kalaspuffar"]').click()
    expect(page.locator("td:has-text('Saras extremt goda kalaspuffar')")).not_to_be_visible()

    








    