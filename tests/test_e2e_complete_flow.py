"""
End-to-End Complete Flow Tests
ทดสอบกระบวนการช้อปปิ้งทั้งหมดแบบ End-to-End
"""

import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestE2ECompleteFlow:
    """Test cases สำหรับ End-to-End flow"""
    
    def test_complete_shopping_flow_standard_user(self, page: Page, base_url: str):
        """ทดสอบกระบวนการช้อปปิ้งทั้งหมด: Login → Browse → Cart → Checkout"""
        # Step 1: Login
        page.goto(base_url)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        expect(page).to_have_url(f"{base_url}/inventory.html")
        print("✓ Step 1: Login successful")
        
        # Step 2: Browse products และเลือกสินค้า
        expect(page.locator(".inventory_item")).to_have_count(6)
        
        # เลือกสินค้า 3 ชิ้น
        page.locator(".btn_inventory").nth(0).click()
        page.locator(".btn_inventory").nth(1).click()
        page.locator(".btn_inventory").nth(2).click()
        
        expect(page.locator(".shopping_cart_badge")).to_have_text("3")
        print("✓ Step 2: Added 3 products to cart")
        
        # Step 3: ดูตะกร้า
        page.click(".shopping_cart_link")
        expect(page).to_have_url(f"{base_url}/cart.html")
        expect(page.locator(".cart_item")).to_have_count(3)
        print("✓ Step 3: Viewed cart")
        
        # Step 4: Checkout - กรอกข้อมูล
        page.click("#checkout")
        expect(page).to_have_url(f"{base_url}/checkout-step-one.html")
        
        page.fill("#first-name", "สมชาย")
        page.fill("#last-name", "ใจดี")
        page.fill("#postal-code", "10110")
        page.click("#continue")
        print("✓ Step 4: Filled checkout information")
        
        # Step 5: ตรวจสอบสรุปคำสั่งซื้อ
        expect(page).to_have_url(f"{base_url}/checkout-step-two.html")
        expect(page.locator(".cart_item")).to_have_count(3)
        
        # ตรวจสอบราคา
        expect(page.locator(".summary_subtotal_label")).to_be_visible()
        expect(page.locator(".summary_tax_label")).to_be_visible()
        expect(page.locator(".summary_total_label")).to_be_visible()
        print("✓ Step 5: Reviewed order summary")
        
        # Step 6: ยืนยันคำสั่งซื้อ
        page.click("#finish")
        expect(page).to_have_url(f"{base_url}/checkout-complete.html")
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        print("✓ Step 6: Order completed successfully")
        
        # Step 7: ตรวจสอบว่าตะกร้าว่าง
        expect(page.locator(".shopping_cart_badge")).not_to_be_visible()
        print("✓ Step 7: Cart is empty after order")
        
        # Step 8: กลับหน้าแรก
        page.click("#back-to-products")
        expect(page).to_have_url(f"{base_url}/inventory.html")
        print("✓ Step 8: Back to products page")
        
        print("\n🎉 Complete shopping flow test passed!")
    
    
    def test_complete_flow_with_product_details_view(self, page: Page, base_url: str):
        """ทดสอบ flow ที่มีการดูรายละเอียดสินค้า"""
        # Login
        page.goto(base_url)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # ดูรายละเอียดสินค้า
        page.locator(".inventory_item_name").first.click()
        expect(page).to_have_url(re.compile(r".*inventory-item\.html.*"))
        
        # เพิ่มสินค้าจากหน้ารายละเอียด
        page.click(".btn_inventory")
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")
        
        # กลับไปหน้าสินค้า
        page.click("#back-to-products")
        
        # เพิ่มสินค้าอีก 1 ชิ้น
        page.locator(".btn_inventory").nth(0).click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("2")
        
        # ดำเนินการ checkout
        page.click(".shopping_cart_link")
        page.click("#checkout")
        
        page.fill("#first-name", "Test")
        page.fill("#last-name", "User")
        page.fill("#postal-code", "12345")
        page.click("#continue")
        
        # สั่งซื้อ
        page.click("#finish")
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        
        print("✓ Complete flow with product details view passed!")
    
    
    def test_add_and_remove_products_before_checkout(self, page: Page, base_url: str):
        """ทดสอบการเพิ่มและลบสินค้าก่อน checkout"""
        # Login
        page.goto(base_url)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # เพิ่มสินค้า 4 ชิ้น
        for i in range(4):
            page.locator(".btn_inventory").nth(i).click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("4")
        
        # ลบสินค้า 2 ชิ้น
        page.locator(".btn_inventory").nth(0).click()
        page.locator(".btn_inventory").nth(0).click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("2")
        
        # ไปหน้าตะกร้า
        page.click(".shopping_cart_link")
        expect(page.locator(".cart_item")).to_have_count(2)
        
        # ลบสินค้า 1 ชิ้นในตะกร้า
        page.locator(".cart_button").first.click()
        expect(page.locator(".cart_item")).to_have_count(1)
        
        # ดำเนินการ checkout
        page.click("#checkout")
        page.fill("#first-name", "John")
        page.fill("#last-name", "Doe")
        page.fill("#postal-code", "90210")
        page.click("#continue")
        
        # ตรวจสอบว่ามีสินค้า 1 ชิ้นในสรุป
        expect(page.locator(".cart_item")).to_have_count(1)
        
        # สั่งซื้อ
        page.click("#finish")
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        
        print("✓ Add and remove products flow passed!")
    
    
    def test_multiple_checkouts_in_same_session(self, page: Page, base_url: str):
        """ทดสอบการ checkout หลายครั้งในเซสชันเดียวกัน"""
        # Login
        page.goto(base_url)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # การซื้อครั้งที่ 1
        page.locator(".btn_inventory").first.click()
        page.click(".shopping_cart_link")
        page.click("#checkout")
        page.fill("#first-name", "First")
        page.fill("#last-name", "Order")
        page.fill("#postal-code", "11111")
        page.click("#continue")
        page.click("#finish")
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        print("✓ First order completed")
        
        # กลับหน้าสินค้า
        page.click("#back-to-products")
        
        # การซื้อครั้งที่ 2
        page.locator(".btn_inventory").nth(1).click()
        page.locator(".btn_inventory").nth(2).click()
        page.click(".shopping_cart_link")
        page.click("#checkout")
        page.fill("#first-name", "Second")
        page.fill("#last-name", "Order")
        page.fill("#postal-code", "22222")
        page.click("#continue")
        page.click("#finish")
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        print("✓ Second order completed")
        
        print("✓ Multiple checkouts flow passed!")
    
    
    def test_sorting_and_filtering_before_purchase(self, page: Page, base_url: str):
        """ทดสอบการเรียงลำดับสินค้าก่อนซื้อ"""
        # Login
        page.goto(base_url)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # เรียงตามราคาจากต่ำไปสูง
        page.select_option(".product_sort_container", "lohi")
        
        # เลือกสินค้าที่ถูกที่สุด
        page.locator(".btn_inventory").first.click()
        
        # เรียงตามราคาจากสูงไปต่ำ
        page.select_option(".product_sort_container", "hilo")
        
        # เลือกสินค้าที่แพงที่สุด
        page.locator(".btn_inventory").first.click()
        
        # ตรวจสอบว่ามี 2 สินค้าในตะกร้า
        expect(page.locator(".shopping_cart_badge")).to_have_text("2")
        
        # ดำเนินการ checkout
        page.click(".shopping_cart_link")
        expect(page.locator(".cart_item")).to_have_count(2)
        
        page.click("#checkout")
        page.fill("#first-name", "Sorted")
        page.fill("#last-name", "Purchase")
        page.fill("#postal-code", "33333")
        page.click("#continue")
        page.click("#finish")
        
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        print("✓ Sorting before purchase flow passed!")


@pytest.mark.e2e
@pytest.mark.smoke
class TestCriticalUserJourneys:
    """ทดสอบ User Journeys ที่สำคัญที่สุด (Smoke Tests)"""
    
    def test_quick_purchase_journey(self, page: Page, base_url: str):
        """ทดสอบการซื้อแบบเร็ว (Smoke Test)"""
        # Login → Add → Checkout → Complete
        page.goto(base_url)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        page.locator(".btn_inventory").first.click()
        page.click(".shopping_cart_link")
        page.click("#checkout")
        
        page.fill("#first-name", "Quick")
        page.fill("#last-name", "Buy")
        page.fill("#postal-code", "99999")
        page.click("#continue")
        page.click("#finish")
        
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        print("✓ Quick purchase journey passed! (Smoke Test)")
    
    
    def test_browse_without_purchase(self, page: Page, base_url: str):
        """ทดสอบการเรียกดูสินค้าโดยไม่ซื้อ"""
        # Login
        page.goto(base_url)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # ดูรายละเอียดสินค้าหลายชิ้น
        for i in range(3):
            page.locator(".inventory_item_name").nth(i).click()
            expect(page).to_have_url(re.compile(r".*inventory-item\.html.*"))
            page.click("#back-to-products")
            expect(page).to_have_url(f"{base_url}/inventory.html")
        
        # Logout
        page.click("#react-burger-menu-btn")
        page.wait_for_selector(".bm-menu", state="visible")
        page.click("#logout_sidebar_link")
        
        expect(page).to_have_url(base_url + "/")
        print("✓ Browse without purchase flow passed!")
