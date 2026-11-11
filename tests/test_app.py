import os
import json
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Base URL from environment variable
BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000")


@pytest.fixture(scope="module")
def driver():
	options = webdriver.ChromeOptions()

	# CI-safe Chrome flags
	options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-gpu")
	options.add_argument("--window-size=1920,1080")

	# Use Google Chrome (not Chromium)
	options.binary_location = "/usr/bin/google-chrome"

	# Let webdriver-manager handle compatible driver
	service = Service(ChromeDriverManager().install())
	browser = webdriver.Chrome(service=service, options=options)
	yield browser
	browser.quit()


def test_app_is_reachable(driver):
	driver.get(BASE_URL)
	assert driver.current_url.startswith(BASE_URL)
