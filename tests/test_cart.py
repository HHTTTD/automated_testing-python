"""
Shopping Cart Tests
ทดสอบ Shopping Cart ของเว็บไซต์ SauceDemo
"""

import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.cart
class TestShoppingCart:
    """Test cases สำหรับ Shopping Cart"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        """Setup: Login ก่อนทดสอบแต่ละ test"""
        self.page = logged_in_page
        expect(self.page).to_have_url("/inventory.html")
    
    
    def test_add_product_to_cart_from_products_page(self):
        """ทดสอบเพิ่มสินค้าลงตะกร้าจากหน้า Products"""
        # คลิกปุ่ม Add to cart สินค้าแรก
        add_button = self.page.locator(".btn_inventory").first
        add_button.click()
        
        # ตรวจสอบว่าปุ่มเปลี่ยนเป็น "Remove"
        expect(add_button).to_have_text("Remove")
        
        # ตรวจสอบว่า cart badge แสดง 1
        expect(self.page.locator(".shopping_cart_badge")).to_have_text("1")
    
    
    def test_add_multiple_products_to_cart(self):
        """ทดสอบเพิ่มหลายสินค้าลงตะกร้า"""
        # เพิ่ม 3 สินค้าลงตะกร้า
        buttons = self.page.locator(".btn_inventory")
        buttons.nth(0).click()
        buttons.nth(1).click()
        buttons.nth(2).click()
        
        # ตรวจสอบว่า cart badge แสดง 3
        expect(self.page.locator(".shopping_cart_badge")).to_have_text("3")
    
    
    def test_remove_product_from_cart_on_products_page(self):
        """ทดสอบลบสินค้าออกจากตะกร้าในหน้า Products"""
        # เพิ่มสินค้าลงตะกร้า
        product_button = self.page.locator(".btn_inventory").first
        product_button.click()
        expect(self.page.locator(".shopping_cart_badge")).to_have_text("1")
        
        # ลบสินค้าออก (คลิก Remove)
        product_button.click()
        
        # ตรวจสอบว่าปุ่มกลับเป็น "Add to cart"
        expect(product_button).to_have_text("Add to cart")
        
        # ตรวจสอบว่า cart badge หายไป
        expect(self.page.locator(".shopping_cart_badge")).not_to_be_visible()
    
    
    def test_add_product_from_product_details_page(self):
        """ทดสอบเพิ่มสินค้าจากหน้ารายละเอียดสินค้า"""
        # เข้าหน้ารายละเอียดสินค้า
        self.page.locator(".inventory_item_name").first.click()
        expect(self.page).to_have_url(re.compile(r".*inventory-item\.html.*"))
        
        # เพิ่มสินค้าลงตะกร้า
        self.page.click(".btn_inventory")
        
        # ตรวจสอบว่าปุ่มเปลี่ยนเป็น "Remove"
        expect(self.page.locator(".btn_inventory")).to_have_text("Remove")
        
        # ตรวจสอบว่า cart badge แสดง 1
        expect(self.page.locator(".shopping_cart_badge")).to_have_text("1")
    
    
    def test_navigate_to_cart_page(self):
        """ทดสอบเข้าหน้า Cart"""
        # เพิ่มสินค้าลงตะกร้า
        self.page.locator(".btn_inventory").first.click()
        
        # คลิกไอคอน cart
        self.page.click(".shopping_cart_link")
        
        # ตรวจสอบว่าเข้าหน้า cart
        expect(self.page).to_have_url("/cart.html")
        expect(self.page.locator(".title")).to_have_text("Your Cart")
    
    
    def test_display_products_in_cart_correctly(self):
        """ทดสอบแสดงสินค้าในตะกร้าถูกต้อง"""
        # ดึงข้อมูลสินค้าแรก
        first_product_name = self.page.locator(".inventory_item_name").first.text_content()
        first_product_price = self.page.locator(".inventory_item_price").first.text_content()
        
        # เพิ่มสินค้าแรกลงตะกร้า
        self.page.locator(".btn_inventory").first.click()
        
        # เข้าหน้า cart
        self.page.click(".shopping_cart_link")
        
        # ตรวจสอบว่าสินค้าในตะกร้าตรงกับที่เพิ่ม
        cart_item = self.page.locator(".cart_item")
        expect(cart_item).to_have_count(1)
        expect(cart_item.locator(".inventory_item_name")).to_have_text(first_product_name)
        expect(cart_item.locator(".inventory_item_price")).to_have_text(first_product_price)
    
    
    def test_remove_product_from_cart_page(self):
        """ทดสอบลบสินค้าจากหน้า Cart"""
        # เพิ่มสินค้าลงตะกร้า
        self.page.locator(".btn_inventory").first.click()
        
        # เข้าหน้า cart
        self.page.click(".shopping_cart_link")
        expect(self.page.locator(".cart_item")).to_have_count(1)
        
        # ลบสินค้า
        self.page.click(".cart_button")
        
        # ตรวจสอบว่าสินค้าหายไปจากตะกร้า
        expect(self.page.locator(".cart_item")).to_have_count(0)
        
        # ตรวจสอบว่า cart badge หายไป
        expect(self.page.locator(".shopping_cart_badge")).not_to_be_visible()
    
    
    def test_continue_shopping(self):
        """ทดสอบ Continue Shopping"""
        # เพิ่มสินค้าและเข้าหน้า cart
        self.page.locator(".btn_inventory").first.click()
        self.page.click(".shopping_cart_link")
        
        # คลิก Continue Shopping
        self.page.click("#continue-shopping")
        
        # ตรวจสอบว่ากลับหน้า products
        expect(self.page).to_have_url("/inventory.html")
        
        # ตรวจสอบว่าสินค้ายังอยู่ในตะกร้า
        expect(self.page.locator(".shopping_cart_badge")).to_have_text("1")
    
    
    def test_proceed_to_checkout(self):
        """ทดสอบ Proceed to Checkout"""
        # เพิ่มสินค้าและเข้าหน้า cart
        self.page.locator(".btn_inventory").first.click()
        self.page.click(".shopping_cart_link")
        
        # คลิก Checkout
        self.page.click("#checkout")
        
        # ตรวจสอบว่าเข้าหน้า checkout
        expect(self.page).to_have_url("/checkout-step-one.html")
        expect(self.page.locator(".title")).to_have_text("Checkout: Your Information")
    
    
    def test_cart_persists_after_logout_and_login(self):
        """ทดสอบว่าตะกร้ายังคงมีสินค้าหลัง Logout/Login"""
        # เพิ่มสินค้าลงตะกร้า
        self.page.locator(".btn_inventory").first.click()
        self.page.locator(".btn_inventory").nth(1).click()
        expect(self.page.locator(".shopping_cart_badge")).to_have_text("2")
        
        # Logout
        self.page.click("#react-burger-menu-btn")
        self.page.wait_for_selector(".bm-menu", state="visible")
        self.page.click("#logout_sidebar_link")
        
        # Login อีกครั้ง
        self.page.fill("#user-name", "standard_user")
        self.page.fill("#password", "secret_sauce")
        self.page.click("#login-button")
        
        # ตรวจสอบว่าตะกร้ายังมีสินค้า 2 ชิ้น
        expect(self.page.locator(".shopping_cart_badge")).to_have_text("2")
