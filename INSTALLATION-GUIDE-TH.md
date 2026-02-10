# 📦 คู่มือการติดตั้ง - Automated Testing with Playwright & Python

## วิธีติดตั้งแบบอัตโนมัติ (แนะนำ)

### สำหรับ Windows

1. **Double-click ไฟล์ `setup.bat`** หรือเปิด Command Prompt/PowerShell แล้วรัน:

```powershell
cd c:\Users\Lenovo\Desktop\Test\Automated_testing\test-02
.\setup.bat
```

Script จะทำการ:
- ✅ ตรวจสอบการติดตั้ง Python
- ✅ สร้าง Virtual Environment
- ✅ ติดตั้ง Python Dependencies
- ✅ ติดตั้ง Playwright Browsers
- ✅ สร้างโฟลเดอร์ที่จำเป็น

**⏱ เวลาที่ใช้:** ประมาณ 5-10 นาที (ขึ้นกับความเร็วอินเทอร์เน็ต)

---

## วิธีติดตั้งด้วยตนเอง

### ขั้นตอนที่ 1: ตรวจสอบ Python

```powershell
python --version
```

ต้องเป็น Python 3.8 หรือสูงกว่า

ถ้ายังไม่มี: ดาวน์โหลดจาก https://www.python.org/downloads/

### ขั้นตอนที่ 2: สร้าง Virtual Environment

```powershell
cd c:\Users\Lenovo\Desktop\Test\Automated_testing\test-02
python -m venv venv
```

### ขั้นตอนที่ 3: เปิดใช้งาน Virtual Environment

```powershell
# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1

# หมายเหตุ: ถ้าเจอ error เรื่อง ExecutionPolicy ใน PowerShell ให้รัน:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

เมื่อสำเร็จ จะเห็น `(venv)` ข้างหน้าใน command line

### ขั้นตอนที่ 4: อัปเกรด pip

```powershell
python -m pip install --upgrade pip
```

### ขั้นตอนที่ 5: ติดตั้ง Python Dependencies

```powershell
pip install -r requirements.txt
```

**Dependencies ที่จะติดตั้ง:**
- `playwright==1.41.0` (29 MB) - Browser automation framework
- `pytest==7.4.3` - Testing framework
- `pytest-playwright==0.4.4` - Pytest plugin for Playwright
- `pytest-html==4.1.1` - HTML report generator
- `python-dotenv==1.0.0` - Environment variables loader

**⏱ เวลาที่ใช้:** 3-7 นาที

### ขั้นตอนที่ 6: ติดตั้ง Playwright Browsers

```powershell
playwright install
```

จะติดตั้ง browsers:
- Chromium (~150 MB)
- Firefox (~80 MB)
- WebKit (~60 MB)

**⏱ เวลาที่ใช้:** 5-10 นาที

### ขั้นตอนที่ 7: ตรวจสอบการติดตั้ง

```powershell
# ตรวจสอบ Playwright
playwright --version

# ตรวจสอบ Pytest
pytest --version

# รัน test ตัวอย่างเพื่อทดสอบ
pytest tests/test_example_quick.py::TestQuickExamples::test_example_1_check_website_title -v
```

---

## การแก้ปัญหาที่พบบ่อย

### 1. Python ไม่พบ (python: command not found)

**สาเหตุ:** Python ไม่ได้ถูกเพิ่มใน PATH

**แก้ไข:**
1. ติดตั้ง Python จาก https://www.python.org
2. เมื่อติดตั้ง ให้เลือก "Add Python to PATH"
3. หรือเพิ่ม PATH ด้วยตนเอง

### 2. pip install ช้ามาก

**สาเหตุ:** เน็ตช้า หรือ PyPI server ช้า

**แก้ไข:** ใช้ mirror ของประเทศไทย
```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. playwright install ล้มเหลว

**สาเหตุ:** สิทธิ์ไม่เพียงพอ หรือ Antivirus บล็อก

**แก้ไข:**
- รัน Command Prompt/PowerShell แบบ Administrator
- ปิด Antivirus ชั่วคราว
- หรือติดตั้ง browser เฉพาะตัว:
  ```powershell
  playwright install chromium
  ```

### 4. ExecutionPolicy error (PowerShell)

**สาเหตุ:** PowerShell บล็อกการรัน script

**แก้ไข:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Import Error: No module named 'playwright'

**สาเหตุ:** Virtual environment ไม่ได้เปิดใช้งาน

**แก้ไข:**
```powershell
venv\Scripts\activate
```

### 6. Browser not found error

**สาเหตุ:** Playwright browsers ไม่ได้ติดตั้ง

**แก้ไข:**
```powershell
playwright install
```

---

## การตรวจสอบว่าติดตั้งสำเร็จ

รันคำสั่งนี้เพื่อตรวจสอบ:

```powershell
# เปิด virtual environment
venv\Scripts\activate

# ตรวจสอบ packages
pip list

# ควรเห็น:
# playwright         1.41.0
# pytest             7.4.3
# pytest-playwright  0.4.4
# pytest-html        4.1.1
# python-dotenv      1.0.0

# รัน test ตัวอย่าง
pytest tests/test_example_quick.py -v --headed
```

---

## ขั้นตอนหลังติดตั้ง

### 1. รัน Test ครั้งแรก

```powershell
# เปิด virtual environment
venv\Scripts\activate

# รัน test ตัวอย่าง
pytest tests/test_example_quick.py -v --headed
```

### 2. ดู Documentation

- 📄 `README.md` - เอกสารหลัก
- 📄 `QUICK-START-TH.md` - คู่มือเริ่มต้นด่วน
- 📄 `GUIDE-TH.md` - คู่มือฉบับสมบูรณ์

### 3. ลองรัน Test ต่างๆ

```powershell
# Login tests
pytest tests/test_login.py -v --headed

# All tests
pytest -v

# Smoke tests
pytest -m smoke -v
```

---

## ทรัพยากรเพิ่มเติม

### เอกสาร
- 🌐 [Playwright Python Documentation](https://playwright.dev/python/)
- 🌐 [Pytest Documentation](https://docs.pytest.org/)
- 🌐 [Python Official Documentation](https://docs.python.org/)

### วิดีโอสอน
- 🎥 [Playwright Tutorial for Beginners](https://www.youtube.com/watch?v=j8MRs3mHBFU)
- 🎥 [Pytest Tutorial](https://www.youtube.com/watch?v=byaxg00Gf9I)

---

## สรุป

**ขั้นตอนสั้นๆ:**

1. ติดตั้ง Python 3.8+
2. สร้าง virtual environment: `python -m venv venv`
3. เปิดใช้งาน: `venv\Scripts\activate`
4. ติดตั้ง dependencies: `pip install -r requirements.txt`
5. ติดตั้ง browsers: `playwright install`
6. รัน test: `pytest -v`

**หรือใช้ setup script:**

```powershell
.\setup.bat
```

---

**Happy Testing! 🎉**
