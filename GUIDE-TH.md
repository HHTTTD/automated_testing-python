# 📚 คู่มือฉบับสมบูรณ์ - Automated Testing with Playwright & Python

## สารบัญ

1. [ภาพรวม](#ภาพรวม)
2. [การติดตั้งและตั้งค่า](#การติดตั้งและตั้งค่า)
3. [โครงสร้างโปรเจค](#โครงสร้างโปรเจค)
4. [การเขียน Test](#การเขียน-test)
5. [Fixtures และ Conftest](#fixtures-และ-conftest)
6. [การรัน Test](#การรัน-test)
7. [Markers และ Tags](#markers-และ-tags)
8. [Best Practices](#best-practices)
9. [การ Debug](#การ-debug)
10. [Tips และ Tricks](#tips-และ-tricks)

---

## ภาพรวม

โปรเจคนี้เป็นตัวอย่างการทำ **Automated Testing** สำหรับเว็บไซต์ [SauceDemo.com](https://www.saucedemo.com) โดยใช้:

- **Playwright**: Framework สำหรับ Browser Automation
- **Python**: ภาษาโปรแกรมมิ่ง
- **Pytest**: Testing Framework สำหรับ Python

### จุดเด่น

✅ รองรับหลาย Browsers (Chromium, Firefox, WebKit)  
✅ รัน Test แบบ Parallel ได้  
✅ มี Fixtures สำหรับใช้ซ้ำ  
✅ สร้าง Report แบบ HTML ได้  
✅ Debug ง่ายด้วย Playwright Inspector  
✅ มี Test Cases ครบถ้วน 54 tests

---

## การติดตั้งและตั้งค่า

### ข้อกำหนดเบื้องต้น

- Python 3.8 หรือสูงกว่า
- pip (Python package manager)
- Git (optional)

### วิธีติดตั้ง

#### วิธีที่ 1: ใช้ Script อัตโนมัติ (Windows)

```bash
# Double-click ไฟล์ setup.bat
# หรือรันจาก Command Prompt:
setup.bat
```

#### วิธีที่ 2: ติดตั้งด้วยตนเอง

```bash
# 1. สร้าง virtual environment
python -m venv venv

# 2. เปิดใช้งาน virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. ติดตั้ง dependencies
pip install -r requirements.txt

# 4. ติดตั้ง Playwright browsers
playwright install
```

### ตรวจสอบการติดตั้ง

```bash
# ตรวจสอบ Playwright
playwright --version

# ตรวจสอบ Pytest
pytest --version

# รัน test ง่ายๆ
pytest tests/test_example_quick.py::TestQuickExamples::test_example_1_check_website_title -v
```

---

## โครงสร้างโปรเจค

```
test-02/
│
├── tests/                          # โฟลเดอร์เก็บ test files
│   ├── __init__.py                # Python package marker
│   ├── test_login.py              # Tests สำหรับ Login
│   ├── test_products.py           # Tests สำหรับ Products
│   ├── test_cart.py               # Tests สำหรับ Shopping Cart
│   ├── test_checkout.py           # Tests สำหรับ Checkout
│   ├── test_e2e_complete_flow.py  # End-to-End Tests
│   └── test_example_quick.py      # ตัวอย่างสำหรับเริ่มต้น
│
├── venv/                           # Virtual environment (ไม่ commit ลง Git)
│
├── screenshots/                    # Screenshots จาก tests (auto-generated)
├── test-results/                   # Test results (auto-generated)
├── playwright-report/              # Playwright report (auto-generated)
│
├── conftest.py                     # Pytest fixtures & configuration
├── pytest.ini                      # Pytest settings
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── setup.bat                       # Setup script (Windows)
├── run-tests.bat                   # Test runner script (Windows)
│
├── README.md                       # เอกสารหลัก
├── QUICK-START-TH.md              # คู่มือเริ่มต้นด่วน
└── GUIDE-TH.md                    # คู่มือฉบับนี้
```

---

## การเขียน Test

### โครงสร้าง Test File

```python
"""
Module docstring - อธิบายว่าไฟล์นี้ทดสอบอะไร
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.marker_name  # Marker สำหรับจัดกลุ่ม
class TestClassName:
    """Test class docstring"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        """Setup ที่รันก่อนแต่ละ test"""
        self.page = logged_in_page
    
    def test_something(self):
        """Test function docstring"""
        # Arrange (เตรียมข้อมูล)
        expected_title = "Products"
        
        # Act (ทำการทดสอบ)
        actual_title = self.page.locator(".title").text_content()
        
        # Assert (ตรวจสอบผลลัพธ์)
        assert actual_title == expected_title
```

### ตัวอย่าง Test แบบง่าย

```python
def test_simple_login(page: Page):
    """ตัวอย่าง test แบบง่าย"""
    # เปิดเว็บไซต์
    page.goto("https://www.saucedemo.com")
    
    # กรอกข้อมูล
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # ตรวจสอบผลลัพธ์
    expect(page).to_have_url(/inventory/)
    expect(page.locator(".title")).to_have_text("Products")
```

### ใช้ Fixtures

```python
def test_with_fixture(page: Page, standard_user: dict):
    """ใช้ fixture ที่กำหนดไว้ใน conftest.py"""
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", standard_user["username"])
    page.fill("#password", standard_user["password"])
    page.click("#login-button")
    
    expect(page).to_have_url(/inventory/)
```

---

## Fixtures และ Conftest

### Fixtures ที่มีอยู่ใน conftest.py

#### 1. `base_url`
```python
@pytest.fixture
def base_url():
    """Base URL ของเว็บไซต์ทดสอบ"""
    return "https://www.saucedemo.com"
```

#### 2. `standard_user`
```python
@pytest.fixture
def standard_user():
    """ข้อมูล standard user"""
    return {
        "username": "standard_user",
        "password": "secret_sauce"
    }
```

#### 3. `logged_in_page`
```python
@pytest.fixture
def logged_in_page(page: Page, standard_user):
    """Page ที่ login แล้ว"""
    login(page, standard_user["username"], standard_user["password"])
    return page
```

### สร้าง Fixture ของตัวเอง

```python
# เพิ่มใน conftest.py
@pytest.fixture
def shopping_cart_with_items(logged_in_page: Page):
    """Page ที่มีสินค้าในตะกร้าแล้ว"""
    page = logged_in_page
    
    # เพิ่มสินค้า 3 ชิ้น
    for i in range(3):
        page.locator(".btn_inventory").nth(i).click()
    
    return page
```

---

## การรัน Test

### คำสั่งพื้นฐาน

```bash
# รัน test ทั้งหมด
pytest

# รัน test แบบละเอียด
pytest -v

# รัน test แบบเห็น browser
pytest --headed

# รัน test แบบ slow motion
pytest --headed --slowmo=1000
```

### รัน Test เฉพาะ

```bash
# รัน test ใน file เฉพาะ
pytest tests/test_login.py -v

# รัน test ใน class เฉพาะ
pytest tests/test_login.py::TestLogin -v

# รัน test function เฉพาะ
pytest tests/test_login.py::TestLogin::test_login_successfully_with_standard_user -v

# รัน test ที่มี keyword
pytest -k "login" -v
pytest -k "successfully" -v
```

### รัน Test บน Browser เฉพาะ

```bash
# Chromium
pytest --browser chromium -v

# Firefox
pytest --browser firefox -v

# WebKit
pytest --browser webkit -v

# หลาย browsers
pytest --browser chromium --browser firefox -v
```

### รัน Test แบบ Parallel

```bash
# ติดตั้ง pytest-xdist
pip install pytest-xdist

# รันแบบ parallel
pytest -n auto -v

# รันด้วย workers จำนวนเฉพาะ
pytest -n 4 -v
```

---

## Markers และ Tags

### Markers ที่มีอยู่

กำหนดไว้ใน `pytest.ini`:

- `@pytest.mark.login` - Tests สำหรับ Login
- `@pytest.mark.products` - Tests สำหรับ Products
- `@pytest.mark.cart` - Tests สำหรับ Cart
- `@pytest.mark.checkout` - Tests สำหรับ Checkout
- `@pytest.mark.e2e` - End-to-End Tests
- `@pytest.mark.smoke` - Smoke Tests (ทดสอบฟีเจอร์หลัก)

### การใช้งาน Markers

```python
@pytest.mark.smoke
@pytest.mark.login
def test_quick_login(page: Page):
    """Test ที่มี 2 markers"""
    pass
```

### รัน Test ตาม Marker

```bash
# รัน login tests
pytest -m login -v

# รัน smoke tests
pytest -m smoke -v

# รัน login หรือ cart tests
pytest -m "login or cart" -v

# รัน login แต่ไม่ใช่ smoke
pytest -m "login and not smoke" -v
```

---

## Best Practices

### 1. ตั้งชื่อ Test ให้ชัดเจน

```python
# ✅ Good
def test_login_successfully_with_standard_user(page: Page):
    pass

# ❌ Bad
def test_1(page: Page):
    pass
```

### 2. ใช้ AAA Pattern

```python
def test_add_product_to_cart(page: Page):
    # Arrange - เตรียมข้อมูล
    page.goto("https://www.saucedemo.com/inventory.html")
    
    # Act - ทำการทดสอบ
    page.locator(".btn_inventory").first.click()
    
    # Assert - ตรวจสอบผลลัพธ์
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
```

### 3. ใช้ Descriptive Assertions

```python
# ✅ Good
expected_count = 6
actual_count = page.locator(".inventory_item").count()
assert actual_count == expected_count, \
    f"Expected {expected_count} products but found {actual_count}"

# ⚠️ OK but less informative
assert page.locator(".inventory_item").count() == 6
```

### 4. ใช้ Page Object Pattern (สำหรับโปรเจคใหญ่)

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
    
    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

# tests/test_login.py
def test_login_with_page_object(page: Page):
    login_page = LoginPage(page)
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url(/inventory/)
```

### 5. ใช้ Fixtures สำหรับ Setup/Teardown

```python
@pytest.fixture
def logged_in_cart_page(logged_in_page: Page):
    """Setup: มีสินค้าในตะกร้าแล้ว"""
    page = logged_in_page
    page.locator(".btn_inventory").first.click()
    page.click(".shopping_cart_link")
    
    yield page  # ใช้ yield เพื่อ cleanup
    
    # Teardown (optional)
    # ทำความสะอาดหลังจบ test
```

### 6. ใช้ pytest.ini สำหรับ Configuration

```ini
[pytest]
# ตั้งค่าพื้นฐาน
testpaths = tests
python_files = test_*.py
python_functions = test_*

# Default options
addopts = 
    -v
    --tb=short
    --headed
```

---

## การ Debug

### 1. ใช้ --headed และ --slowmo

```bash
pytest tests/test_login.py --headed --slowmo=1000 -v
```

### 2. ใช้ print() หรือ logging

```python
def test_with_logging(page: Page):
    page.goto("https://www.saucedemo.com")
    
    # พิมพ์ข้อมูล
    print(f"Current URL: {page.url}")
    print(f"Page title: {page.title()}")
    
    page.fill("#user-name", "standard_user")
    print("Filled username")
```

### 3. ใช้ Python Debugger (pdb)

```bash
# หยุดที่ test ที่ล้มเหลว
pytest tests/test_login.py --pdb

# หยุดที่จุดที่กำหนด
```

```python
def test_with_breakpoint(page: Page):
    page.goto("https://www.saucedemo.com")
    
    # หยุดที่นี่
    import pdb; pdb.set_trace()
    
    page.fill("#user-name", "standard_user")
```

### 4. ใช้ Playwright Inspector

```bash
# Windows PowerShell
$env:PWDEBUG=1
pytest tests/test_login.py

# Linux/Mac
PWDEBUG=1 pytest tests/test_login.py
```

### 5. ดู Screenshots และ Videos

```bash
# Screenshots และ Videos จะถูกสร้างอัตโนมัติเมื่อ test ล้มเหลว
# ดูใน test-results/ folder
```

---

## Tips และ Tricks

### 1. รัน Test เฉพาะที่ล้มเหลว

```bash
# รัน test ครั้งแรก
pytest -v

# รันเฉพาะที่ล้มเหลว
pytest --lf -v  # --last-failed

# รัน test ที่ล้มเหลวก่อน จากนั้นรันที่เหลือ
pytest --ff -v  # --failed-first
```

### 2. Stop ทันทีเมื่อเจอ test ล้มเหลว

```bash
# หยุดทันทีที่ test ล้มเหลว
pytest -x -v

# หยุดหลังจาก test ล้มเหลว 3 ครั้ง
pytest --maxfail=3 -v
```

### 3. เพิ่ม Timeout

```bash
# ติดตั้ง pytest-timeout
pip install pytest-timeout

# ตั้ง timeout 60 วินาที
pytest --timeout=60 -v
```

### 4. สร้าง HTML Report ที่สวยงาม

```bash
# HTML Report แบบธรรมดา
pytest --html=report.html --self-contained-html -v

# Allure Report (สวยกว่า แต่ต้องติดตั้ง Allure)
pip install allure-pytest
pytest --alluredir=./allure-results
allure serve ./allure-results
```

### 5. ใช้ Parametrize สำหรับ Test หลายกรณี

```python
@pytest.mark.parametrize("username,password,should_succeed", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("invalid_user", "wrong_password", False),
])
def test_login_scenarios(page: Page, username, password, should_succeed):
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")
    
    if should_succeed:
        expect(page).to_have_url(/inventory/)
    else:
        expect(page.locator('[data-test="error"]')).to_be_visible()
```

### 6. ใช้ conftest.py สำหรับ Setup ที่ใช้ซ้ำ

```python
# conftest.py ในโฟลเดอร์ tests/
@pytest.fixture(scope="session")
def test_data():
    """Load test data ครั้งเดียวสำหรับทั้ง session"""
    return {
        "valid_users": ["standard_user", "performance_glitch_user"],
        "invalid_users": ["locked_out_user", "invalid_user"],
    }
```

### 7. ใช้ Skip และ Xfail

```python
@pytest.mark.skip(reason="Feature not implemented yet")
def test_new_feature(page: Page):
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_linux_only(page: Page):
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_with_known_bug(page: Page):
    # Test ที่คาดว่าจะล้มเหลว
    pass
```

---

## สรุป

โปรเจคนี้เป็นตัวอย่างที่ครบถ้วนสำหรับการทำ Automated Testing ด้วย Playwright และ Python

### ข้อดี
- ✅ เขียนง่าย อ่านง่าย
- ✅ รองรับหลาย browsers
- ✅ รัน test เร็ว (parallel support)
- ✅ มี fixtures ที่ใช้ซ้ำได้
- ✅ Debug ง่าย
- ✅ Documentation ครบถ้วน

### แหล่งเรียนรู้เพิ่มเติม

- 📖 [Playwright Python Documentation](https://playwright.dev/python/)
- 📖 [Pytest Documentation](https://docs.pytest.org/)
- 📖 [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- 🎥 [Playwright YouTube Channel](https://www.youtube.com/@Playwrightdev)

---

**Happy Testing! 🎭🐍**
