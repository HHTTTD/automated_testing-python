"""
Checkout Process Tests
ทดสอบกระบวนการ Checkout ของเว็บไซต์ SauceDemo
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.checkout
class TestCheckout:
    """Test cases สำหรับกระบวนการ Checkout"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        """Setup: Login และเพิ่มสินค้าในตะกร้าก่อนทดสอบ"""
        self.page = logged_in_page
        
        # เพิ่มสินค้าลงตะกร้า
        self.page.locator(".btn_inventory").first.click()
        
        # เข้าหน้า cart
        self.page.click(".shopping_cart_link")
        
        # เข้าหน้า checkout
        self.page.click("#checkout")
        
        # ตรวจสอบว่าอยู่หน้า checkout step 1
        expect(self.page).to_have_url("/checkout-step-one.html")
    
    
    def test_display_checkout_information_form(self):
        """ทดสอบแสดงฟอร์มข้อมูลการจัดส่ง"""
        # ตรวจสอบ title
        expect(self.page.locator(".title")).to_have_text("Checkout: Your Information")
        
        # ตรวจสอบ form fields
        expect(self.page.locator("#first-name")).to_be_visible()
        expect(self.page.locator("#last-name")).to_be_visible()
        expect(self.page.locator("#postal-code")).to_be_visible()
        expect(self.page.locator("#continue")).to_be_visible()
        expect(self.page.locator("#cancel")).to_be_visible()
    
    
    def test_fill_information_successfully(self):
        """ทดสอบกรอกข้อมูลสำเร็จ"""
        # กรอกข้อมูล
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        
        # คลิก Continue
        self.page.click("#continue")
        
        # ตรวจสอบว่าไปหน้า checkout step 2
        expect(self.page).to_have_url("/checkout-step-two.html")
        expect(self.page.locator(".title")).to_have_text("Checkout: Overview")
    
    
    def test_show_error_for_empty_first_name(self):
        """ทดสอบแสดง Error เมื่อ First Name ว่าง"""
        # กรอกข้อมูลยกเว้น first name
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        
        # คลิก Continue
        self.page.click("#continue")
        
        # ตรวจสอบ error message
        error_message = self.page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("First Name is required")
    
    
    def test_show_error_for_empty_last_name(self):
        """ทดสอบแสดง Error เมื่อ Last Name ว่าง"""
        # กรอกข้อมูลยกเว้น last name
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#postal-code", "10110")
        
        # คลิก Continue
        self.page.click("#continue")
        
        # ตรวจสอบ error message
        error_message = self.page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Last Name is required")
    
    
    def test_show_error_for_empty_postal_code(self):
        """ทดสอบแสดง Error เมื่อ Postal Code ว่าง"""
        # กรอกข้อมูลยกเว้น postal code
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        
        # คลิก Continue
        self.page.click("#continue")
        
        # ตรวจสอบ error message
        error_message = self.page.locator('[data-test="error"]')
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Postal Code is required")
    
    
    def test_cancel_checkout(self):
        """ทดสอบยกเลิกการ Checkout"""
        # คลิก Cancel
        self.page.click("#cancel")
        
        # ตรวจสอบว่ากลับหน้า cart
        expect(self.page).to_have_url("/cart.html")
    
    
    def test_display_order_summary_correctly(self):
        """ทดสอบแสดงสรุปคำสั่งซื้อถูกต้อง"""
        # กรอกข้อมูลและไปหน้า overview
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        self.page.click("#continue")
        
        # ตรวจสอบว่ามีสินค้าในสรุป
        expect(self.page.locator(".cart_item")).to_have_count(1)
        
        # ตรวจสอบว่ามีข้อมูลการชำระเงิน
        expect(self.page.locator(".summary_subtotal_label")).to_be_visible()
        expect(self.page.locator(".summary_tax_label")).to_be_visible()
        expect(self.page.locator(".summary_total_label")).to_be_visible()
    
    
    def test_calculate_total_price_correctly(self):
        """ทดสอบคำนวณราคารวมถูกต้อง"""
        # กรอกข้อมูลและไปหน้า overview
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        self.page.click("#continue")
        
        # ดึงราคา
        subtotal_text = self.page.locator(".summary_subtotal_label").text_content()
        tax_text = self.page.locator(".summary_tax_label").text_content()
        total_text = self.page.locator(".summary_total_label").text_content()
        
        # แปลงเป็นตัวเลข
        subtotal = float(subtotal_text.split("$")[1])
        tax = float(tax_text.split("$")[1])
        total = float(total_text.split("$")[1])
        
        # ตรวจสอบว่าคำนวณถูกต้อง
        expected_total = round(subtotal + tax, 2)
        assert total == expected_total, f"ราคารวมไม่ถูกต้อง: {total} != {expected_total}"
    
    
    def test_cancel_checkout_from_overview(self):
        """ทดสอบยกเลิกจากหน้า Overview"""
        # กรอกข้อมูลและไปหน้า overview
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        self.page.click("#continue")
        
        # คลิก Cancel
        self.page.click("#cancel")
        
        # ตรวจสอบว่ากลับหน้า products
        expect(self.page).to_have_url("/inventory.html")
    
    
    def test_complete_order_successfully(self):
        """ทดสอบสั่งซื้อสำเร็จ"""
        # กรอกข้อมูลและไปหน้า overview
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        self.page.click("#continue")
        
        # คลิก Finish
        self.page.click("#finish")
        
        # ตรวจสอบหน้า complete
        expect(self.page).to_have_url("/checkout-complete.html")
        expect(self.page.locator(".complete-header")).to_have_text("Thank you for your order!")
        expect(self.page.locator(".complete-text")).to_be_visible()
    
    
    def test_cart_is_empty_after_order_complete(self):
        """ทดสอบว่าตะกร้าว่างหลังสั่งซื้อเสร็จ"""
        # กรอกข้อมูลและไปหน้า overview
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        self.page.click("#continue")
        
        # สั่งซื้อ
        self.page.click("#finish")
        
        # ตรวจสอบว่า cart badge หายไป
        expect(self.page.locator(".shopping_cart_badge")).not_to_be_visible()
    
    
    def test_back_to_home_after_order_complete(self):
        """ทดสอบกลับหน้าแรกหลังสั่งซื้อเสร็จ"""
        # กรอกข้อมูลและไปหน้า overview
        self.page.fill("#first-name", "สมชาย")
        self.page.fill("#last-name", "ใจดี")
        self.page.fill("#postal-code", "10110")
        self.page.click("#continue")
        
        # สั่งซื้อ
        self.page.click("#finish")
        
        # คลิก Back Home
        self.page.click("#back-to-products")
        
        # ตรวจสอบว่ากลับหน้า products
        expect(self.page).to_have_url("/inventory.html")
