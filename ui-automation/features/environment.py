from selenium.webdriver.chrome.options import Options
import os


def before_all(context):
    pass  # Driver is initialised per-scenario in the @given step


def after_all(context):
    # Safety cleanup in case the browser wasn't closed by the test
    if hasattr(context, "driver"):
        context.driver.quit()