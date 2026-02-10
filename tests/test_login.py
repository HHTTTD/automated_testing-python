"""
Login Functionality Tests
ทดสอบการ Login ของเว็บไซต์ SauceDemo
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.login
class TestLogin:
    """Test cases สำหรับการ Login"""
    
    def test_display_login_page_correctly(self, page: Page, base_url: str):
        """ทดสอบว่าหน้า Login แสดงผลถูกต้อง"""
        # เปิดเว็บไซต์
        page.goto(base_url)
        
        # ตรวจสอบ title
        expect(page).to_have_title("Swag Labs")
        
        # ตรวจสอบ login form elements
        expect(page.locator("#user-name")).to_be_visible()
        expect(page.locator("#password")).to_be_visible()
        expect(page.locator("#login-button")).to_be_visible()
    
    
    def test_login_successfully_with_standard_user(self, page: Page, base_url: str, standard_user: dict):
        """ทดสอบ Login สำเร็จด้วย standard_user"""
        # เปิดหน้า Login
        page.goto(base_url)
        
        # กรอกข้อมูล
        page.fill("#user-name", standard_user["username"])
        page.fill("#password", standard_user["password"])
        
        # คลิกปุ่ม Login
        page.click("#login-button")
        
        # ตรวจสอบว่า Login สำเร็จ
        expect(page).to_have_url(f"{base_url}/inventory.html")
        expect(page.locator(".title")).to_have_text("Products")
        expect(page.locator(".inventory_list")).to_be_visible()
    
    
    def test_show_error_message_for_locked_out_user(self, page: Page, base_url: str, locked_user: dict):
        """ทดสอบแสดง Error สำหรับ locked_out_user"""
        # เปิดหน้า Login
        page.goto(base_url)
        
        # พยายาม Login ด้วย locked out user
        page.fill("#user-name", locked_user["username"])
        page.fill("#password", locked_user["password"])
        page.click("#login-button")
        
        # ตรวจสอบ error message
        error_message = page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Sorry, this user has been locked out")
    
    
    def test_show_error_message_for_invalid_credentials(self, page: Page, base_url: str):
        """ทดสอบแสดง Error สำหรับ username/password ผิด"""
        # เปิดหน้า Login
        page.goto(base_url)
        
        # พยายาม Login ด้วยข้อมูลผิด
        page.fill("#user-name", "invalid_user")
        page.fill("#password", "wrong_password")
        page.click("#login-button")
        
        # ตรวจสอบ error message
        error_message = page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Username and password do not match")
    
    
    def test_show_error_message_for_empty_username(self, page: Page, base_url: str):
        """ทดสอบแสดง Error เมื่อ username ว่าง"""
        # เปิดหน้า Login
        page.goto(base_url)
        
        # กรอกแค่ password
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # ตรวจสอบ error message
        error_message = page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Username is required")
    
    
    def test_show_error_message_for_empty_password(self, page: Page, base_url: str):
        """ทดสอบแสดง Error เมื่อ password ว่าง"""
        # เปิดหน้า Login
        page.goto(base_url)
        
        # กรอกแค่ username
        page.fill("#user-name", "standard_user")
        page.click("#login-button")
        
        # ตรวจสอบ error message
        error_message = page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Password is required")
    
    
    def test_close_error_message(self, page: Page, base_url: str):
        """ทดสอบปิด Error message ได้"""
        # เปิดหน้า Login
        page.goto(base_url)
        
        # สร้าง error message
        page.fill("#user-name", "invalid_user")
        page.fill("#password", "wrong_password")
        page.click("#login-button")
        
        # ตรวจสอบว่า error message แสดง
        error_message = page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        
        # ปิด error message
        page.click(".error-button")
        
        # ตรวจสอบว่า error message หายไป
        expect(error_message).not_to_be_visible()
