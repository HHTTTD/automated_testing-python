"""
Products Page Tests
ทดสอบหน้า Products ของเว็บไซต์ SauceDemo
"""

import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.products
class TestProducts:
    """Test cases สำหรับหน้า Products"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        """Setup: Login ก่อนทดสอบแต่ละ test"""
        self.page = logged_in_page
        # ตรวจสอบว่าอยู่หน้า products
        expect(self.page).to_have_url("/inventory.html")
    
    
    def test_display_all_products(self):
        """ทดสอบแสดงสินค้าทั้งหมด (6 items)"""
        # ตรวจสอบจำนวนสินค้า
        product_items = self.page.locator(".inventory_item")
        expect(product_items).to_have_count(6)
        
        # ตรวจสอบว่าสินค้าแรกมี elements ครบ
        first_product = product_items.first
        expect(first_product.locator(".inventory_item_name")).to_be_visible()
        expect(first_product.locator(".inventory_item_desc")).to_be_visible()
        expect(first_product.locator(".inventory_item_price")).to_be_visible()
        expect(first_product.locator("button")).to_be_visible()
    
    
    def test_sort_products_by_name_a_to_z(self):
        """ทดสอบเรียงสินค้าตามชื่อ A-Z"""
        # เลือก sort option
        self.page.select_option(".product_sort_container", "az")
        
        # ดึงชื่อสินค้าทั้งหมด
        product_names = self.page.locator(".inventory_item_name").all_text_contents()
        
        # ตรวจสอบว่าเรียงตามลำดับ A-Z
        sorted_names = sorted(product_names)
        assert product_names == sorted_names, "สินค้าไม่ได้เรียงตาม A-Z"
    
    
    def test_sort_products_by_name_z_to_a(self):
        """ทดสอบเรียงสินค้าตามชื่อ Z-A"""
        # เลือก sort option
        self.page.select_option(".product_sort_container", "za")
        
        # ดึงชื่อสินค้าทั้งหมด
        product_names = self.page.locator(".inventory_item_name").all_text_contents()
        
        # ตรวจสอบว่าเรียงตามลำดับ Z-A
        sorted_names = sorted(product_names, reverse=True)
        assert product_names == sorted_names, "สินค้าไม่ได้เรียงตาม Z-A"
    
    
    def test_sort_products_by_price_low_to_high(self):
        """ทดสอบเรียงสินค้าตามราคา (ต่ำ-สูง)"""
        # เลือก sort option
        self.page.select_option(".product_sort_container", "lohi")
        
        # ดึงราคาสินค้าทั้งหมด
        price_texts = self.page.locator(".inventory_item_price").all_text_contents()
        prices = [float(price.replace("$", "")) for price in price_texts]
        
        # ตรวจสอบว่าเรียงจากต่ำไปสูง
        sorted_prices = sorted(prices)
        assert prices == sorted_prices, "สินค้าไม่ได้เรียงตามราคาจากต่ำไปสูง"
    
    
    def test_sort_products_by_price_high_to_low(self):
        """ทดสอบเรียงสินค้าตามราคา (สูง-ต่ำ)"""
        # เลือก sort option
        self.page.select_option(".product_sort_container", "hilo")
        
        # ดึงราคาสินค้าทั้งหมด
        price_texts = self.page.locator(".inventory_item_price").all_text_contents()
        prices = [float(price.replace("$", "")) for price in price_texts]
        
        # ตรวจสอบว่าเรียงจากสูงไปต่ำ
        sorted_prices = sorted(prices, reverse=True)
        assert prices == sorted_prices, "สินค้าไม่ได้เรียงตามราคาจากสูงไปต่ำ"
    
    
    def test_view_product_details(self):
        """ทดสอบดูรายละเอียดสินค้า"""
        # คลิกที่สินค้าแรก
        self.page.locator(".inventory_item_name").first.click()
        
        # ตรวจสอบว่าเข้าหน้ารายละเอียดสินค้า
        expect(self.page).to_have_url(re.compile(r".*inventory-item\.html.*"))
        
        # ตรวจสอบ elements ในหน้ารายละเอียด
        expect(self.page.locator(".inventory_details_name")).to_be_visible()
        expect(self.page.locator(".inventory_details_desc")).to_be_visible()
        expect(self.page.locator(".inventory_details_price")).to_be_visible()
        expect(self.page.locator(".btn_inventory")).to_be_visible()
    
    
    def test_back_from_product_details(self):
        """ทดสอบกลับจากหน้ารายละเอียดสินค้า"""
        # เข้าหน้ารายละเอียดสินค้า
        self.page.locator(".inventory_item_name").first.click()
        expect(self.page).to_have_url(re.compile(r".*inventory-item\.html.*"))
        
        # คลิกปุ่ม Back
        self.page.click("#back-to-products")
        
        # ตรวจสอบว่ากลับมาหน้า products
        expect(self.page).to_have_url("/inventory.html")
        expect(self.page.locator(".inventory_list")).to_be_visible()
    
    
    def test_open_menu(self):
        """ทดสอบเปิด Menu"""
        # คลิกปุ่ม menu
        self.page.click("#react-burger-menu-btn")
        
        # ตรวจสอบว่า menu เปิด
        menu = self.page.locator(".bm-menu")
        expect(menu).to_be_visible()
        
        # ตรวจสอบ menu items
        expect(self.page.locator("#inventory_sidebar_link")).to_be_visible()
        expect(self.page.locator("#about_sidebar_link")).to_be_visible()
        expect(self.page.locator("#logout_sidebar_link")).to_be_visible()
    
    
    def test_logout_from_menu(self):
        """ทดสอบ Logout จาก Menu"""
        # เปิด menu
        self.page.click("#react-burger-menu-btn")
        self.page.wait_for_selector(".bm-menu", state="visible")
        
        # คลิก Logout
        self.page.click("#logout_sidebar_link")
        
        # ตรวจสอบว่ากลับมาหน้า Login
        expect(self.page).to_have_url("https://www.saucedemo.com/")
        expect(self.page.locator("#login-button")).to_be_visible()
