# 🚀 เริ่มต้นที่นี่! - START HERE

## ยินดีต้อนรับสู่ Automated Testing Project!

โปรเจคนี้เป็น **Automated Testing** สำหรับเว็บไซต์ SauceDemo.com  
ใช้ **Playwright + Python** ในการทดสอบ

---

## ⚡ เริ่มใช้งานด่วน (3 ขั้นตอน)

### ขั้นตอนที่ 1: ติดตั้ง

**Double-click ไฟล์นี้:**
```
setup.bat
```

หรือเปิด Command Prompt/PowerShell แล้วรัน:
```powershell
.\setup.bat
```

⏱ ใช้เวลา: 5-10 นาที

---

### ขั้นตอนที่ 2: รัน Test

**Double-click ไฟล์นี้:**
```
run-tests.bat
```

หรือเปิด Command Prompt/PowerShell แล้วรัน:
```powershell
.\run-tests.bat
```

จากนั้นเลือกเมนู:
- กด `9` = รัน test ตัวอย่าง (แนะนำสำหรับครั้งแรก!)
- กด `3` = รัน login tests
- กด `1` = รัน test ทั้งหมด

---

### ขั้นตอนที่ 3: ดูผลลัพธ์

Test จะรันและแสดงผลลัพธ์ในหน้าจอ

✅ = ผ่าน  
❌ = ไม่ผ่าน

---

## 📚 มีคำถามหรือต้องการเรียนรู้เพิ่มเติม?

อ่านเอกสารเหล่านี้:

### สำหรับมือใหม่ 👶
1. **`README.md`** - เริ่มต้นที่นี่
2. **`QUICK-START-TH.md`** - คู่มือด่วน

### สำหรับผู้ใช้ทั่วไป 👨‍💻
3. **`GUIDE-TH.md`** - คู่มือฉบับสมบูรณ์
4. **`INSTALLATION-GUIDE-TH.md`** - แก้ปัญหาการติดตั้ง

### สำหรับทุกคน 📋
5. **`SUMMARY-TH.md`** - สรุปโปรเจค

---

## 🎯 Test Coverage

โปรเจคนี้มี **54 test cases** ครอบคลุม:

- ✅ Login (7 tests)
- ✅ Products (9 tests)
- ✅ Shopping Cart (11 tests)
- ✅ Checkout (13 tests)
- ✅ End-to-End (7 tests)
- ✅ Examples (7 tests)

---

## 💡 Tips สำหรับมือใหม่

### 1. รัน Test ตัวอย่างก่อน

```powershell
# เปิด virtual environment
venv\Scripts\activate

# รัน test ตัวอย่างแบบเห็น browser
pytest tests/test_example_quick.py -v --headed
```

### 2. ดู Test แบบ Slow Motion

```powershell
pytest tests/test_example_quick.py -v --headed --slowmo=1000
```

เห็นการทำงานแบบช้าๆ เข้าใจง่ายขึ้น!

### 3. รัน Test เฉพาะตัวเดียว

```powershell
pytest tests/test_login.py -v --headed
```

---

## 🆘 เจอปัญหา?

### ปัญหา: setup.bat ไม่ทำงาน

**แก้ไข:** ตรวจสอบว่าติดตั้ง Python แล้ว
```powershell
python --version
```

ถ้ายังไม่มี → ดาวน์โหลดจาก https://www.python.org

---

### ปัญหา: Test ล้มเหลว

**แก้ไข:** รันแบบ debug
```powershell
venv\Scripts\activate
pytest tests/test_login.py -v --headed --slowmo=2000
```

---

### ปัญหา: ติดตั้งช้า

**เหตุผล:** Playwright ต้องดาวน์โหลด browsers (~300 MB)  
**วิธีแก้:** รอให้เสร็จ หรืออ่าน `INSTALLATION-GUIDE-TH.md`

---

## 📂 โครงสร้างโปรเจค

```
test-02/
├── tests/              # โฟลเดอร์เก็บ test files
│   ├── test_login.py   # ทดสอบ Login
│   ├── test_products.py # ทดสอบ Products
│   ├── test_cart.py    # ทดสอบ Cart
│   └── ...
├── setup.bat           # Script ติดตั้ง
├── run-tests.bat       # Script รัน test
├── README.md           # เอกสารหลัก
└── ...
```

---

## 🎓 เรียนรู้เพิ่มเติม

### ลำดับการอ่าน (แนะนำ)

1. **START-HERE.md** ← คุณอยู่ที่นี่
2. **README.md** - ภาพรวมโปรเจค
3. **QUICK-START-TH.md** - คู่มือเริ่มต้น
4. **GUIDE-TH.md** - เรียนรู้ลึก

### ไฟล์ Test ตัวอย่าง

- `tests/test_example_quick.py` - ตัวอย่างพื้นฐาน
- `tests/test_login.py` - ตัวอย่างจริง

---

## ✨ คำสั่งที่ใช้บ่อย

```powershell
# เปิด virtual environment
venv\Scripts\activate

# รัน test ทั้งหมด
pytest -v

# รัน test แบบเห็น browser
pytest --headed -v

# รัน test เฉพาะไฟล์
pytest tests/test_login.py -v

# สร้าง HTML report
pytest --html=report.html --self-contained-html -v
```

---

## 🎉 พร้อมแล้ว!

เริ่มต้นเลยตอนนี้:

### วิธีที่ 1: ใช้ Scripts (ง่ายที่สุด)
1. Double-click `setup.bat`
2. รอให้ติดตั้งเสร็จ
3. Double-click `run-tests.bat`
4. เลือกเมนู และกด Enter

### วิธีที่ 2: ใช้ Command Line
```powershell
# 1. ติดตั้ง
.\setup.bat

# 2. รัน test
venv\Scripts\activate
pytest tests/test_example_quick.py -v --headed
```

---

## 💬 สรุป

- 🎯 โปรเจคนี้มี 54 test cases สำหรับ SauceDemo.com
- 🚀 ใช้ Playwright + Python
- 📚 มีเอกสารภาษาไทยครบถ้วน
- 🛠️ มี scripts สำหรับติดตั้งและรัน test
- ✅ ใช้งานง่าย เหมาะกับทุกระดับ

---

**Happy Testing! 🎭🐍**

---

## 🔗 Quick Links

- 📄 [README.md](README.md) - เอกสารหลัก
- 📄 [QUICK-START-TH.md](QUICK-START-TH.md) - คู่มือเริ่มต้น
- 📄 [GUIDE-TH.md](GUIDE-TH.md) - คู่มือฉบับเต็ม
- 📄 [INSTALLATION-GUIDE-TH.md](INSTALLATION-GUIDE-TH.md) - การติดตั้ง
- 📄 [SUMMARY-TH.md](SUMMARY-TH.md) - สรุปโปรเจค

---

**เวอร์ชัน:** 1.0.0  
**สร้างเมื่อ:** February 10, 2026  
**ภาษา:** Python 3.10+  
**Framework:** Playwright + Pytest
