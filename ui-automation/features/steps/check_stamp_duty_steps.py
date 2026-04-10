# features/steps/check_stamp_duty_steps.py
from behave import given, when, then
from selenium.webdriver.common.by import By

from utils.helpers import (
    # Driver
    get_chrome_driver,
    # Element
    wait_for_clickable,
    # Page-specific elements
    get_vehicle_input,
    get_calculate_button,
    # Navigation
    wait_for_redirect,
    # Modal
    get_modal,
    get_modal_title,
    get_modal_heading,
    get_table_cell_value,
    get_modal_note,
    get_modal_link,
    get_modal_footer_button,
    # Assertions
    format_currency,
    is_valid_dollar_amount,
    log_assert,
    print_popup_text,
)


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given(u'I am on the Service NSW motor vehicle stamp duty page')
def step_open_service_nsw(context):
    context.driver = get_chrome_driver()
    context.driver.get(
        "https://www.service.nsw.gov.au/transaction/check-motor-vehicle-stamp-duty"
    )


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when(u'I click the "Check Online" button')
def step_click_check_online(context):
    btn = wait_for_clickable(
        context.driver, By.PARTIAL_LINK_TEXT, "Check online", timeout=20
    )
    btn.click()


@when(u'I select "Yes" for NSW residency')
def step_select_nsw_residency(context):
    # Actual input is visually hidden — click the label to trigger it
    label = wait_for_clickable(
        context.driver, By.CSS_SELECTOR, "label[for='passenger_Y']"
    )
    label.click()


@when(u'I enter a vehicle amount of {amount:d}')
def step_enter_vehicle_amount(context, amount):
    context.vehicle_amount = amount  # stored for purchase price assertion later
    vehicle_input = get_vehicle_input(context.driver)
    vehicle_input.clear()
    vehicle_input.send_keys(str(amount))


@when(u'I click the "Calculate" button')
def step_click_calculate(context):
    get_calculate_button(context.driver).click()


# ---------------------------------------------------------------------------
# Then — redirect
# ---------------------------------------------------------------------------

@then(u'I should be redirected to the Revenue NSW calculator page')
def step_redirect_to_revenue_calculator(context):
    original_windows = set(context.driver.window_handles)
    wait_for_redirect(context.driver, original_windows, "revenue.nsw.gov.au")
    assert "revenue.nsw.gov.au" in context.driver.current_url, \
        f"Not redirected to Revenue NSW. URL: {context.driver.current_url}"


# ---------------------------------------------------------------------------
# Then — popup: existence
# ---------------------------------------------------------------------------

@then(u'I should see the stamp duty result popup')
def step_verify_result_popup(context):
    popup = get_modal(context.driver)
    assert popup.is_displayed(), "Stamp duty result popup not found"
    context.popup = popup
    print_popup_text(popup)


# ---------------------------------------------------------------------------
# Then — popup: title and heading
# ---------------------------------------------------------------------------

@then(u'the popup title should be "{title}"')
def step_popup_title(context, title):
    actual = get_modal_title(context.driver)
    log_assert("Popup title", actual, title)
    assert actual == title, f"Expected popup title '{title}', got '{actual}'"


@then(u'the popup heading should be "{heading}"')
def step_popup_heading(context, heading):
    actual = get_modal_heading(context.driver)
    log_assert("Popup heading", actual, heading)
    assert heading in actual, f"Expected heading '{heading}' in '{actual}'"


# ---------------------------------------------------------------------------
# Then — popup: table row assertions
# ---------------------------------------------------------------------------

@then(u'the popup details table should show "{label}" as "{expected_value}"')
def step_popup_table_row(context, label, expected_value):
    actual = get_table_cell_value(context.driver, label)
    log_assert(f"Table row '{label}'", actual, expected_value)
    assert actual == expected_value, (
        f"Expected '{label}' = '{expected_value}', got '{actual}'"
    )


@then(u'the popup details table should show the correct purchase price')
def step_popup_correct_price(context):
    assert hasattr(context, 'vehicle_amount'), \
        "vehicle_amount not set — run 'I enter a vehicle amount of <n>' first"
    expected = format_currency(context.vehicle_amount)
    actual = get_table_cell_value(context.driver, "Purchase price or value")
    log_assert("Purchase price or value", actual, expected)
    assert actual == expected, (
        f"Expected purchase price '{expected}', got '{actual}'"
    )


@then(u'the popup details table should show a valid duty payable amount')
def step_popup_duty_amount(context):
    actual = get_table_cell_value(context.driver, "Duty payable")
    log_assert("Duty payable", actual)
    assert is_valid_dollar_amount(actual), (
        f"Expected 'Duty payable' to be a dollar amount like $1,650.00, got '{actual}'"
    )


# ---------------------------------------------------------------------------
# Then — popup: note and links
# ---------------------------------------------------------------------------

@then(u'the popup should contain the note "{note_text}"')
def step_popup_note(context, note_text):
    actual = get_modal_note(context.driver)
    log_assert("Note text", actual)
    assert note_text in actual, (
        f"Expected note to contain '{note_text}', got '{actual}'"
    )


@then(u'the popup should have a "{link_text}" link')
def step_popup_link(context, link_text):
    link = get_modal_link(context.driver, link_text)
    log_assert(f"Link '{link_text}'", link.get_attribute("href"))
    assert link.is_displayed(), f"'{link_text}' link not visible in popup"


@then(u'the popup should have a "{button_text}" button')
def step_popup_button(context, button_text):
    btn = get_modal_footer_button(context.driver, button_text)
    log_assert(f"Button '{button_text}'", "found in modal-footer")
    assert btn.is_displayed(), f"'{button_text}' button not visible in popup footer"


# ---------------------------------------------------------------------------
# Then — close
# ---------------------------------------------------------------------------

@then(u'close the browser')
def step_close_browser(context):
    context.driver.quit()