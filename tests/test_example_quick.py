"""
Quick Example Tests
ไฟล์นี้เป็นตัวอย่างการเขียน test แบบง่ายๆ สำหรับเริ่มต้นเรียนรู้ Playwright กับ Python
"""

import pytest
from playwright.sync_api import Page, expect


class TestQuickExamples:
    """ตัวอย่าง Tests สำหรับเริ่มต้น"""
    
    def test_example_1_check_website_title(self, page: Page):
        """ตัวอย่างที่ 1: ตรวจสอบ Title ของเว็บไซต์"""
        page.goto("https://www.saucedemo.com")
        expect(page).to_have_title("Swag Labs")
        print("✓ Website title is correct!")
    
    
    def test_example_2_simple_login(self, page: Page):
        """ตัวอย่างที่ 2: การ Login พื้นฐาน"""
        # เปิดเว็บไซต์
        page.goto("https://www.saucedemo.com")
        
        # กรอกข้อมูล
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        
        # คลิกปุ่ม Login
        page.click("#login-button")
        
        # ตรวจสอบว่า Login สำเร็จ
        import re
        expect(page).to_have_url(re.compile(".*inventory.*"))
        print("✓ Login successful!")
    
    
    def test_example_3_take_screenshot(self, page: Page):
        """ตัวอย่างที่ 3: การถ่ายภาพหน้าจอ"""
        page.goto("https://www.saucedemo.com")
        
        # ถ่ายภาพหน้าจอ
        page.screenshot(path="screenshots/login-page.png")
        print("✓ Screenshot saved to screenshots/login-page.png")
    
    
    def test_example_4_wait_for_element(self, page: Page):
        """ตัวอย่างที่ 4: การรอ Element"""
        page.goto("https://www.saucedemo.com")
        
        # รอจนกว่า element จะปรากฏ
        page.wait_for_selector("#login-button")
        
        # ตรวจสอบว่า element มองเห็นได้
        expect(page.locator("#login-button")).to_be_visible()
        print("✓ Login button is visible!")
    
    
    def test_example_5_count_products_after_login(self, page: Page):
        """ตัวอย่างที่ 5: การนับจำนวน Elements"""
        # Login
        page.goto("https://www.saucedemo.com")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # นับจำนวนสินค้า
        product_count = page.locator(".inventory_item").count()
        print(f"Found {product_count} products")
        
        # ตรวจสอบว่ามี 6 สินค้า
        assert product_count == 6, f"Expected 6 products, but found {product_count}"
        print("✓ Product count is correct!")
    
    
    def test_example_6_get_text_from_element(self, page: Page):
        """ตัวอย่างที่ 6: การดึงข้อความจาก Element"""
        page.goto("https://www.saucedemo.com")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # ดึงชื่อสินค้าแรก
        first_product_name = page.locator(".inventory_item_name").first.text_content()
        print(f"First product: {first_product_name}")
        
        # ตรวจสอบว่าชื่อสินค้าไม่ว่าง
        assert first_product_name != "", "Product name should not be empty"
        print("✓ Product name retrieved successfully!")
    
    
    def test_example_7_custom_timeout(self, page: Page):
        """ตัวอย่างที่ 7: การใช้ Custom Timeout"""
        # ตั้งค่า timeout
        page.set_default_timeout(10000)  # 10 วินาที
        
        page.goto("https://www.saucedemo.com", wait_until="networkidle")
        
        expect(page.locator("#login-button")).to_be_visible(timeout=5000)
        print("✓ Page loaded within timeout!")


# วิธีรันไฟล์นี้:
# 
# 1. รัน test ทั้งหมดในไฟล์นี้:
#    pytest tests/test_example_quick.py -v
# 
# 2. รันแบบเห็น browser:
#    pytest tests/test_example_quick.py -v --headed
# 
# 3. รัน test เดียว:
#    pytest tests/test_example_quick.py::TestQuickExamples::test_example_2_simple_login -v
# 
# 4. รันใน debug mode:
#    pytest tests/test_example_quick.py -v --headed --slowmo=1000
