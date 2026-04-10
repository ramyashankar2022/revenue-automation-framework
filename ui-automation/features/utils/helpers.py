# features/utils/helpers.py
"""
Reusable utility library for Selenium + Behave automation.

Organised into 5 sections:
  1. Driver Utilities       — Chrome driver setup
  2. Element Utilities      — Wait, find, click helpers
  3. Page-specific Elements — Vehicle input, calculate button
  4. Navigation Utilities   — Redirect and window switching
  5. Modal Utilities        — Popup element accessors
  6. Assertion Utilities    — Formatting, validation, logging
"""
import os
import re

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------------------------------------------------
# Timeouts — CI servers are slower so we give them more time
# ---------------------------------------------------------------------------
IS_CI = os.environ.get('CI', 'false').lower() == 'true'

SHORT_WAIT  = 20  if IS_CI else 10   # for single element waits
LONG_WAIT   = 40  if IS_CI else 20   # for navigation / redirects
MULTI_WAIT  = 30  if IS_CI else 10   # for multi-selector fallback searches


# ===========================================================================
# 1. DRIVER UTILITIES
# ===========================================================================

def get_chrome_driver():
    """
    Create and return a configured Chrome driver.
    - Runs headless in CI (GitHub Actions sets CI=true automatically)
    - Runs with visible browser window when run locally
    """
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    if os.environ.get('CI'):
        options.add_argument("--headless=new")

    # Selenium Manager (4.6+) handles ChromeDriver automatically
    driver = Chrome(options=options)
    driver.maximize_window()
    return driver


# ===========================================================================
# 2. ELEMENT UTILITIES
# ===========================================================================

def wait_for_clickable(driver, by, selector, timeout=SHORT_WAIT):
    """
    Wait until a single element is clickable and return it.

    Usage:
        btn = wait_for_clickable(driver, By.CSS_SELECTOR, "button.submit")
        btn.click()
    """
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )


def wait_for_visible(driver, by, selector, timeout=SHORT_WAIT):
    """
    Wait until a single element is visible and return it.

    Usage:
        popup = wait_for_visible(driver, By.CSS_SELECTOR, "div.modal")
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )


def wait_for_present(driver, by, selector, timeout=SHORT_WAIT):
    """
    Wait until a single element is present in the DOM and return it.

    Usage:
        input_el = wait_for_present(driver, By.ID, "vehicleValue")
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def find_first_clickable(driver, selectors, timeout=MULTI_WAIT):
    """
    Try a list of (By, selector) pairs in order and return the first
    clickable element found. Returns None if nothing matched.

    Usage:
        btn = find_first_clickable(driver, [
            (By.XPATH, '//button[text()="Submit"]'),
            (By.CSS_SELECTOR, "button[type='submit']"),
        ])
    """
    per_timeout = max(1, timeout // len(selectors))
    for by, selector in selectors:
        try:
            el = WebDriverWait(driver, per_timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            if el:
                return el
        except Exception:
            continue
    return None


def find_first_present(driver, selectors, timeout=MULTI_WAIT):
    """
    Try a list of (By, selector) pairs in order and return the first
    element present in the DOM. Returns None if nothing matched.

    Usage:
        input_el = find_first_present(driver, [
            (By.XPATH, '//input[@id="vehicleValue"]'),
            (By.CSS_SELECTOR, "input[type='text']"),
        ])
    """
    per_timeout = max(1, timeout // len(selectors))
    for by, selector in selectors:
        try:
            el = WebDriverWait(driver, per_timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            if el:
                return el
        except Exception:
            continue
    return None


# ===========================================================================
# 3. PAGE-SPECIFIC ELEMENT HELPERS
# ===========================================================================

def get_vehicle_input(driver, timeout=SHORT_WAIT):
    """
    Find and return the vehicle amount input field using multiple fallback selectors.
    Raises AssertionError with a clear message if the field cannot be found.

    Usage:
        vehicle_input = get_vehicle_input(driver)
        vehicle_input.clear()
        vehicle_input.send_keys("50000")
    """
    selectors = [
        (By.XPATH, '//input[@id="vehicleValue"]'),
        (By.XPATH, '//input[@name="vehicleValue"]'),
        (By.CSS_SELECTOR, "input[id*='vehicle']"),
        (By.CSS_SELECTOR, "input[name*='vehicle']"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.CSS_SELECTOR, "input[type='number']"),
    ]
    vehicle_input = find_first_present(driver, selectors, timeout=timeout)
    assert vehicle_input is not None, (
        f"Could not find vehicle amount input.\n"
        f"URL: {driver.current_url} | Title: {driver.title}"
    )
    return vehicle_input


def get_calculate_button(driver, timeout=SHORT_WAIT):
    """
    Find and return the Calculate button using multiple fallback selectors.
    Raises AssertionError with a clear message if the button cannot be found.

    Usage:
        btn = get_calculate_button(driver)
        btn.click()
    """
    selectors = [
        (By.XPATH, '//button[contains(normalize-space(),"Calculate")]'),
        (By.XPATH, '//input[@type="submit" and contains(@value,"Calculate")]'),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, '//input[@type="submit"]'),
    ]
    btn = find_first_clickable(driver, selectors, timeout=timeout)
    assert btn is not None, (
        f"Could not find Calculate button.\n"
        f"URL: {driver.current_url} | Title: {driver.title}"
    )
    return btn


# ===========================================================================
# 4. NAVIGATION UTILITIES
# ===========================================================================

def wait_for_redirect(driver, original_windows, expected_url_fragment, timeout=LONG_WAIT):
    """
    Wait for either:
      - A new browser tab to open, OR
      - The current URL to change to contain expected_url_fragment

    If a new tab opened, automatically switches to it.
    Waits for page to fully load (readyState === 'complete').

    Usage:
        original_windows = set(driver.window_handles)
        wait_for_redirect(driver, original_windows, "revenue.nsw.gov.au")
    """
    def redirected(d):
        if set(d.window_handles) - original_windows:
            return True
        return expected_url_fragment in d.current_url

    WebDriverWait(driver, timeout).until(redirected)

    new_windows = set(driver.window_handles) - original_windows
    if new_windows:
        driver.switch_to.window(new_windows.pop())

    WebDriverWait(driver, timeout).until(
        lambda d: expected_url_fragment in d.current_url
        and d.execute_script("return document.readyState") == "complete"
    )


# ===========================================================================
# 4. MODAL UTILITIES
# ===========================================================================

def get_modal(driver, selector="div.modal-content", timeout=LONG_WAIT):
    """
    Wait for and return the modal/popup container element.

    Usage:
        popup = get_modal(driver)
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )


def get_modal_title(driver):
    """
    Return the text of the modal title element (h4.modal-title).

    Usage:
        title = get_modal_title(driver)  # e.g. "Calculation"
    """
    return driver.find_element(By.CSS_SELECTOR, "h4.modal-title").text.strip()


def get_modal_heading(driver):
    """
    Return the text of the h4 heading inside modal body.

    Usage:
        heading = get_modal_heading(driver)  # e.g. "Motor vehicle registration"
    """
    return driver.find_element(
        By.XPATH, '//div[contains(@class,"modal-body")]//h4'
    ).text.strip()


def get_table_cell_value(driver, label):
    """
    Return the value cell text from a TableApp table matching the given label.

    Usage:
        value = get_table_cell_value(driver, "Purchase price or value")
        # Returns e.g. "$50,000.00"
    """
    xpath = (
        f'//table[contains(@class,"TableApp")]'
        f'//td[contains(normalize-space(text()),"{label}")]'
        f'/following-sibling::td'
    )
    return driver.find_element(By.XPATH, xpath).text.strip()


def get_modal_note(driver):
    """
    Return text of the Note paragraph inside the modal body.

    Usage:
        note = get_modal_note(driver)
        # Returns e.g. "Note: All amounts are in Australian dollars."
    """
    return driver.find_element(
        By.XPATH, '//div[contains(@class,"modal-body")]//p[contains(.,"Note:")]'
    ).text.strip()


def get_modal_link(driver, link_text):
    """
    Return the anchor element matching link_text inside the modal body.

    Usage:
        link = get_modal_link(driver, "contact us")
        href = link.get_attribute("href")
    """
    return driver.find_element(
        By.XPATH,
        f'//div[contains(@class,"modal-body")]//a[contains(normalize-space(),"{link_text}")]'
    )


def get_modal_footer_button(driver, button_text):
    """
    Return the button element matching button_text inside the modal footer.

    Usage:
        btn = get_modal_footer_button(driver, "Close")
    """
    return driver.find_element(
        By.XPATH,
        f'//div[contains(@class,"modal-footer")]//button[contains(normalize-space(),"{button_text}")]'
    )


# ===========================================================================
# 5. ASSERTION UTILITIES
# ===========================================================================

def format_currency(amount):
    """
    Format an integer amount as an Australian dollar string.

    Usage:
        format_currency(50000)  →  "$50,000.00"
        format_currency(1650)   →  "$1,650.00"
    """
    return f"${amount:,.2f}"


def is_valid_dollar_amount(value):
    """
    Return True if value matches a dollar amount format like $1,650.00 or $24,100.00.

    Usage:
        is_valid_dollar_amount("$1,650.00")  →  True
        is_valid_dollar_amount("abc")        →  False
    """
    return bool(re.compile(r'^\$[\d,]+\.\d{2}$').match(value))


def log_assert(label, actual, expected=None):
    """
    Print a formatted assertion log line to the console.

    Usage:
        log_assert("Popup title", actual, expected)
        # Prints: [ASSERT] Popup title → 'Calculation' (expected 'Calculation')

        log_assert("Duty payable", actual)
        # Prints: [ASSERT] Duty payable → '$1,600.00'
    """
    if expected is not None:
        print(f"\n[ASSERT] {label} → '{actual}' (expected '{expected}')")
    else:
        print(f"\n[ASSERT] {label} → '{actual}'")


def print_popup_text(popup):
    """
    Print the full popup text content to the console for debugging.

    Usage:
        print_popup_text(popup_element)
    """
    print("\n" + "=" * 60)
    print("POPUP FULL TEXT:")
    print("=" * 60)
    print(popup.text)
    print("=" * 60 + "\n")