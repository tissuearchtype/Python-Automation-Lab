"""
Saves a timestamped screenshot into reports/screenshots/. Used both on
test failure (see tests/conftest.py) and anywhere a test wants visual
proof of a step (cart contents, search results, etc.).
"""

import os
import time


def take_screenshot(driver, name):
    screenshots_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "reports",
        "screenshots",
    )
    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() else "_" for c in name)
    file_path = os.path.join(screenshots_dir, f"{safe_name}_{timestamp}.png")

    driver.save_screenshot(file_path)
    return file_path
