# Automated Testing for Swag Labs (SauceDemo.com) - Python Version

โปรเจคนี้เป็น Automated Testing สำหรับเว็บไซต์ [Swag Labs](https://www.saucedemo.com) โดยใช้ **Playwright** และ **Python**

## 📋 สารบัญ

- [การติดตั้ง](#การติดตั้ง)
- [โครงสร้างโปรเจค](#โครงสร้างโปรเจค)
- [การรัน Test](#การรัน-test)
- [Test Cases](#test-cases)
- [User Credentials](#user-credentials)

## 🚀 การติดตั้ง

### ข้อกำหนดเบื้องต้น
- Python 3.8 หรือสูงกว่า
- pip (Python package manager)

### ขั้นตอนการติดตั้ง

1. สร้าง Virtual Environment (แนะนำ):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

3. ติดตั้ง Playwright browsers:
```bash
playwright install
```

## 📁 โครงสร้างโปรเจค

```
test-02/
├── tests/
│   ├── __init__.py
│   ├── test_login.py              # ทดสอบการ Login
│   ├── test_products.py           # ทดสอบหน้า Products
│   ├── test_cart.py               # ทดสอบ Shopping Cart
│   ├── test_checkout.py           # ทดสอบการ Checkout
│   ├── test_e2e_complete_flow.py  # ทดสอบ End-to-End ทั้งหมด
│   └── test_example_quick.py      # ตัวอย่างสำหรับเริ่มต้น
├── conftest.py                     # Pytest configuration & fixtures
├── pytest.ini                      # Pytest settings
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # เอกสารนี้
```

## ▶️ การรัน Test

### รัน Test ทั้งหมด
```bash
pytest
```

### รัน Test แบบแสดง Browser (Headed mode)
```bash
pytest --headed
```

### รัน Test เฉพาะไฟล์
```bash
pytest tests/test_login.py -v
```

### รัน Test เฉพาะ Class
```bash
pytest tests/test_login.py::TestLogin -v
```

### รัน Test เฉพาะ Function
```bash
pytest tests/test_login.py::TestLogin::test_login_successfully_with_standard_user -v
```

### รัน Test ตาม Marker
```bash
# รัน login tests
pytest -m login -v

# รัน smoke tests
pytest -m smoke -v

# รัน e2e tests
pytest -m e2e -v
```

### รัน Test บน Browser เฉพาะ
```bash
# Chromium
pytest --browser chromium -v

# Firefox
pytest --browser firefox -v

# WebKit (Safari)
pytest --browser webkit -v

# รันบนทุก browsers
pytest --browser chromium --browser firefox --browser webkit -v
```

### รัน Test แบบ Parallel (เร็วขึ้น)
```bash
# ติดตั้ง pytest-xdist ก่อน
pip install pytest-xdist

# รันแบบ parallel
pytest -n auto
```

### รัน Test แบบ Slow Motion (Debug)
```bash
pytest --headed --slowmo=1000  # หน่วงเวลา 1000ms ต่อ action
```

### สร้าง HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### ดู Test Coverage
```bash
pip install pytest-cov
pytest --cov=tests --cov-report=html
```

## 📝 Test Cases

### 1. Login Tests (`test_login.py`)
- ✅ แสดงหน้า Login ได้ถูกต้อง
- ✅ Login สำเร็จด้วย standard_user
- ✅ แสดง Error สำหรับ locked_out_user
- ✅ แสดง Error สำหรับ username/password ผิด
- ✅ แสดง Error เมื่อ username หรือ password ว่าง
- ✅ ปิด Error message ได้

**จำนวน:** 7 test cases

### 2. Products Tests (`test_products.py`)
- ✅ แสดงสินค้าทั้งหมด (6 items)
- ✅ เรียงสินค้าตามชื่อ (A-Z, Z-A)
- ✅ เรียงสินค้าตามราคา (ต่ำ-สูง, สูง-ต่ำ)
- ✅ ดูรายละเอียดสินค้า
- ✅ กลับจากหน้ารายละเอียดสินค้า
- ✅ เปิด Menu และ Logout

**จำนวน:** 9 test cases

### 3. Cart Tests (`test_cart.py`)
- ✅ เพิ่มสินค้าลงตะกร้า
- ✅ เพิ่มหลายสินค้าลงตะกร้า
- ✅ ลบสินค้าออกจากตะกร้า
- ✅ แสดงสินค้าในตะกร้าถูกต้อง
- ✅ Continue Shopping
- ✅ Proceed to Checkout
- ✅ ตะกร้ายังคงมีสินค้าหลัง Logout/Login

**จำนวน:** 11 test cases

### 4. Checkout Tests (`test_checkout.py`)
- ✅ แสดงฟอร์มข้อมูลการจัดส่ง
- ✅ กรอกข้อมูลสำเร็จ
- ✅ แสดง Error เมื่อข้อมูลไม่ครบ
- ✅ คำนวณราคารวมถูกต้อง
- ✅ ยกเลิกการ Checkout
- ✅ สั่งซื้อสำเร็จ
- ✅ ตะกร้าว่างหลังสั่งซื้อ

**จำนวน:** 13 test cases

### 5. End-to-End Tests (`test_e2e_complete_flow.py`)
- ✅ ทดสอบการช้อปปิ้งทั้งหมด (Login → Browse → Cart → Checkout)
- ✅ ทดสอบ flow ที่มีการดูรายละเอียดสินค้า
- ✅ ทดสอบการเพิ่มและลบสินค้าก่อน checkout
- ✅ ทดสอบ checkout หลายครั้งในเซสชันเดียว
- ✅ ทดสอบการเรียงลำดับสินค้าก่อนซื้อ
- ✅ ทดสอบการซื้อแบบเร็ว (Smoke Test)
- ✅ ทดสอบการเรียกดูสินค้าโดยไม่ซื้อ

**จำนวน:** 7 test cases

### 6. Example Tests (`test_example_quick.py`)
- ✅ ตัวอย่างพื้นฐานสำหรับเริ่มต้นเรียนรู้

**จำนวน:** 7 test cases

**รวมทั้งหมด: 54 test cases**

## 👤 User Credentials

เว็บไซต์ SauceDemo มี Test Users หลายแบบ:

| Username | Password | Description |
|----------|----------|-------------|
| `standard_user` | `secret_sauce` | User ปกติ (ใช้ได้ทุกฟีเจอร์) |
| `locked_out_user` | `secret_sauce` | User ที่ถูกล็อค |
| `problem_user` | `secret_sauce` | User ที่มีปัญหา UI |
| `performance_glitch_user` | `secret_sauce` | User ที่มีปัญหาด้าน Performance |
| `error_user` | `secret_sauce` | User ที่เจอ Error บางอย่าง |
| `visual_user` | `secret_sauce` | User ที่มีปัญหา Visual |

## 📊 Test Reports

### HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### Allure Report (ติดตั้งเพิ่มเติม)
```bash
pip install allure-pytest
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## 🛠️ Configuration

### Pytest Configuration (`pytest.ini`)
- **Browsers**: Chromium, Firefox, WebKit
- **Timeouts**: ตั้งค่าตาม default ของ Playwright
- **Screenshots**: บันทึกเมื่อ Test ล้มเหลว
- **Videos**: บันทึกเมื่อ Test ล้มเหลว
- **Traces**: บันทึกเมื่อ Test ล้มเหลว

### Fixtures (`conftest.py`)
- `base_url`: URL พื้นฐานของเว็บไซต์
- `standard_user`: ข้อมูล standard user
- `logged_in_page`: Page ที่ login แล้ว
- และอื่นๆ

## 💡 Tips

1. ใช้ `--headed` เพื่อดูการทำงานของ Browser
2. ใช้ `--slowmo=1000` เพื่อ Debug แบบทีละขั้นตอน
3. ใช้ `-v` หรือ `-vv` เพื่อดู output แบบละเอียด
4. ใช้ `-k "keyword"` เพื่อรัน test ที่มีคำค้นหา
5. ใช้ `--pdb` เพื่อเข้า debugger เมื่อ test ล้มเหลว
6. ดู [Playwright Python Documentation](https://playwright.dev/python/docs/intro) สำหรับข้อมูลเพิ่มเติม

## 🔧 การ Debug

### Playwright Inspector
```bash
# เปิด Playwright Inspector
PWDEBUG=1 pytest tests/test_login.py

# Windows PowerShell
$env:PWDEBUG=1
pytest tests/test_login.py
```

### Python Debugger
```bash
pytest --pdb  # หยุดที่ test ที่ล้มเหลว
```

### Trace Viewer
```bash
# เปิด trace viewer หลังจากรัน test
playwright show-trace trace.zip
```

## 📚 เอกสารเพิ่มเติม

- 📄 [QUICK-START-TH.md](QUICK-START-TH.md) - คู่มือเริ่มต้นด่วนภาษาไทย
- 🌐 [Playwright Python Docs](https://playwright.dev/python/)
- 🌐 [Pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing

หากพบปัญหาหรือต้องการเพิ่ม test cases:
1. Fork repository นี้
2. สร้าง branch ใหม่
3. เพิ่ม tests
4. ทดสอบให้แน่ใจว่าผ่านทุก test
5. สร้าง Pull Request

## 📄 License

MIT License

## ✨ Author

สร้างด้วย ❤️ โดยใช้ Playwright และ Python

---

**Happy Testing! 🎉**
"# automated_testing-python" 
