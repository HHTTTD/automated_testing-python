"""
Playwright Pytest Configuration
ไฟล์นี้ใช้สำหรับตั้งค่า fixtures และ hooks สำหรับ Playwright tests
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    กำหนดการตั้งค่า browser context
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "ignore_https_errors": True,
    }


@pytest.fixture
def standard_user():
    """
    ข้อมูล standard user สำหรับ login
    """
    return {
        "username": "standard_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def locked_user():
    """
    ข้อมูล locked out user
    """
    return {
        "username": "locked_out_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def problem_user():
    """
    ข้อมูล problem user
    """
    return {
        "username": "problem_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def performance_glitch_user():
    """
    ข้อมูล performance glitch user
    """
    return {
        "username": "performance_glitch_user",
        "password": "secret_sauce"
    }


def login(page: Page, username: str, password: str):
    """
    Helper function สำหรับ login
    """
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")
    
    # รอให้โหลดเสร็จ
    page.wait_for_load_state("networkidle")


@pytest.fixture
def logged_in_page(page: Page, standard_user):
    """
    Fixture ที่ให้ page ที่ login แล้ว
    """
    login(page, standard_user["username"], standard_user["password"])
    return page


# Hooks
def pytest_configure(config):
    """
    Hook ที่รันก่อนเริ่ม test suite
    """
    try:
        print("\n🚀 เริ่มต้นรัน Playwright Tests สำหรับ SauceDemo.com")
    except:
        print("\nStarting Playwright Tests for SauceDemo.com")
    print("=" * 70)


def pytest_unconfigure(config):
    """
    Hook ที่รันหลังจบ test suite
    """
    print("\n" + "=" * 70)
    try:
        print("✅ รัน Tests เสร็จสิ้น!")
    except:
        print("Tests completed!")
