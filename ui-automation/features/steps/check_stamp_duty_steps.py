# features/steps/check_stamp_duty_steps.py
import os
import re
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_table_cell_value(driver, label):
    """Return the value cell text from TableApp for a given label."""
    xpath = (
        f'//table[contains(@class,"TableApp")]'
        f'//td[contains(normalize-space(text()),"{label}")]'
        f'/following-sibling::td'
    )
    return driver.find_element(By.XPATH, xpath).text.strip()


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given(u'I am on the Service NSW motor vehicle stamp duty page')
def step_open_service_nsw(context):
    options = Options()

    # Run headless in CI (GitHub Actions sets CI=true automatically)
    # Runs with a visible browser window when run locally
    if os.environ.get('CI'):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

    context.driver = Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    context.driver.maximize_window()
    context.driver.get(
        "https://www.service.nsw.gov.au/transaction/check-motor-vehicle-stamp-duty"
    )


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when(u'I click the "Check Online" button')
def step_click_check_online(context):
    driver = context.driver
    check_online_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Check online"))
    )
    check_online_button.click()


@when(u'I select "Yes" for NSW residency')
def step_select_nsw_residency(context):
    driver = context.driver
    # Actual input is visually hidden — click the label to trigger it
    yes_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='passenger_Y']"))
    )
    yes_label.click()


@when(u'I enter a vehicle amount of {amount:d}')
def step_enter_vehicle_amount(context, amount):
    context.vehicle_amount = amount  # stored for purchase price assertion later
    driver = context.driver

    selectors = [
        (By.XPATH, '//input[@id="vehicleValue"]'),
        (By.XPATH, '//input[@name="vehicleValue"]'),
        (By.CSS_SELECTOR, "input[id*='vehicle']"),
        (By.CSS_SELECTOR, "input[name*='vehicle']"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.CSS_SELECTOR, "input[type='number']"),
    ]

    vehicle_input = None
    for by, selector in selectors:
        try:
            el = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((by, selector))
            )
            if el:
                vehicle_input = el
                break
        except Exception:
            continue

    assert vehicle_input is not None, (
        f"Could not find vehicle amount input.\n"
        f"URL: {driver.current_url} | Title: {driver.title}"
    )
    vehicle_input.clear()
    vehicle_input.send_keys(str(amount))


@when(u'I click the "Calculate" button')
def step_click_calculate(context):
    driver = context.driver
    selectors = [
        (By.XPATH, '//button[contains(normalize-space(),"Calculate")]'),
        (By.XPATH, '//input[@type="submit" and contains(@value,"Calculate")]'),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, '//input[@type="submit"]'),
    ]
    calculate_btn = None
    for by, selector in selectors:
        try:
            calculate_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((by, selector))
            )
            if calculate_btn:
                break
        except Exception:
            continue

    assert calculate_btn is not None, (
        f"Could not find Calculate button.\n"
        f"URL: {driver.current_url} | Title: {driver.title}"
    )
    calculate_btn.click()


# ---------------------------------------------------------------------------
# Then — redirect
# ---------------------------------------------------------------------------

@then(u'I should be redirected to the Revenue NSW calculator page')
def step_redirect_to_revenue_calculator(context):
    driver = context.driver
    original_windows = set(driver.window_handles)

    def redirected(d):
        if set(d.window_handles) - original_windows:
            return True
        return "revenue.nsw.gov.au" in d.current_url

    WebDriverWait(driver, 20).until(redirected)

    new_windows = set(driver.window_handles) - original_windows
    if new_windows:
        driver.switch_to.window(new_windows.pop())

    WebDriverWait(driver, 20).until(
        lambda d: "revenue.nsw.gov.au" in d.current_url
        and d.execute_script("return document.readyState") == "complete"
    )

    assert "revenue.nsw.gov.au" in driver.current_url, \
        f"Not redirected to Revenue NSW. URL: {driver.current_url}"


# ---------------------------------------------------------------------------
# Then — popup: existence
# ---------------------------------------------------------------------------

@then(u'I should see the stamp duty result popup')
def step_verify_result_popup(context):
    driver = context.driver
    popup = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal-content"))
    )
    assert popup.is_displayed(), "Stamp duty result popup (div.modal-content) not found"
    context.popup = popup

    print("\n" + "=" * 60)
    print("POPUP FULL TEXT:")
    print("=" * 60)
    print(popup.text)
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Then — popup: title and heading
# ---------------------------------------------------------------------------

@then(u'the popup title should be "{title}"')
def step_popup_title(context, title):
    driver = context.driver
    title_el = driver.find_element(By.CSS_SELECTOR, "h4.modal-title")
    actual = title_el.text.strip()
    print(f"\n[ASSERT] Popup title → '{actual}'")
    assert actual == title, f"Expected popup title '{title}', got '{actual}'"


@then(u'the popup heading should be "{heading}"')
def step_popup_heading(context, heading):
    driver = context.driver
    heading_el = driver.find_element(
        By.XPATH, '//div[contains(@class,"modal-body")]//h4'
    )
    actual = heading_el.text.strip()
    print(f"\n[ASSERT] Popup heading → '{actual}'")
    assert heading in actual, f"Expected heading '{heading}' in '{actual}'"


# ---------------------------------------------------------------------------
# Then — popup: table row assertions
# ---------------------------------------------------------------------------

@then(u'the popup details table should show "{label}" as "{expected_value}"')
def step_popup_table_row(context, label, expected_value):
    driver = context.driver
    actual = get_table_cell_value(driver, label)
    print(f"\n[ASSERT] Table row '{label}' → '{actual}'")
    assert actual == expected_value, (
        f"Expected '{label}' = '{expected_value}', got '{actual}'"
    )


@then(u'the popup details table should show the correct purchase price')
def step_popup_correct_price(context):
    assert hasattr(context, 'vehicle_amount'), \
        "vehicle_amount not set — run 'I enter a vehicle amount of <n>' first"
    # 50000 → "$50,000.00"
    expected = f"${context.vehicle_amount:,.2f}"
    driver = context.driver
    actual = get_table_cell_value(driver, "Purchase price or value")
    print(f"\n[ASSERT] Purchase price or value → '{actual}' (expected '{expected}')")
    assert actual == expected, (
        f"Expected purchase price '{expected}', got '{actual}'"
    )


@then(u'the popup details table should show a valid duty payable amount')
def step_popup_duty_amount(context):
    driver = context.driver
    actual = get_table_cell_value(driver, "Duty payable")
    print(f"\n[ASSERT] Duty payable → '{actual}'")
    dollar_pattern = re.compile(r'^\$[\d,]+\.\d{2}$')
    assert dollar_pattern.match(actual), (
        f"Expected 'Duty payable' to be a dollar amount like $1,650.00, got '{actual}'"
    )


# ---------------------------------------------------------------------------
# Then — popup: note and links
# ---------------------------------------------------------------------------

@then(u'the popup should contain the note "{note_text}"')
def step_popup_note(context, note_text):
    driver = context.driver
    note_el = driver.find_element(
        By.XPATH, '//div[contains(@class,"modal-body")]//p[contains(.,"Note:")]'
    )
    actual = note_el.text.strip()
    print(f"\n[ASSERT] Note text → '{actual}'")
    assert note_text in actual, f"Expected note to contain '{note_text}', got '{actual}'"


@then(u'the popup should have a "{link_text}" link')
def step_popup_link(context, link_text):
    driver = context.driver
    link = driver.find_element(
        By.XPATH,
        f'//div[contains(@class,"modal-body")]//a[contains(normalize-space(),"{link_text}")]'
    )
    href = link.get_attribute("href")
    print(f"\n[ASSERT] Link '{link_text}' → href='{href}'")
    assert link.is_displayed(), f"'{link_text}' link not visible in popup"


@then(u'the popup should have a "{button_text}" button')
def step_popup_button(context, button_text):
    driver = context.driver
    btn = driver.find_element(
        By.XPATH,
        f'//div[contains(@class,"modal-footer")]//button[contains(normalize-space(),"{button_text}")]'
    )
    print(f"\n[ASSERT] Button '{button_text}' found in modal-footer")
    assert btn.is_displayed(), f"'{button_text}' button not visible in popup footer"


# ---------------------------------------------------------------------------
# Then — close
# ---------------------------------------------------------------------------

@then(u'close the browser')
def step_close_browser(context):
    context.driver.quit()