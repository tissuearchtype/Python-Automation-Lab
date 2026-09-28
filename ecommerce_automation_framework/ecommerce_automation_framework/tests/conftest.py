"""
Shared PyTest fixtures.

- `driver` fixture: creates one browser per test, always quits it after,
  even if the test fails or raises.
- `pytest_runtest_makereport` hook: on any test FAILURE, automatically
  saves a screenshot into reports/screenshots/ and attaches its path to
  the HTML report. This is what the assignment calls
  "Screenshots on Failure".
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import get_driver
from utils.screenshot_util import take_screenshot


@pytest.fixture
def driver():
    drv = get_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            screenshot_path = take_screenshot(driver_fixture, item.name)
            if hasattr(report, "extra"):
                pass
            extra = getattr(report, "extra", [])
            try:
                from pytest_html import extras
                extra.append(extras.image(screenshot_path))
                report.extra = extra
            except ImportError:
                pass
            print(f"\nScreenshot saved on failure: {screenshot_path}")
