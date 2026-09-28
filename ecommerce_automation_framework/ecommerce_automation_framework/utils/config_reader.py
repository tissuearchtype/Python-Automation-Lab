"""
Reads config/config.yaml once and exposes its values to the rest of
the framework. Keeping this in one place means the URL, browser choice,
waits, and test credentials are never hard-coded inside a test or page.
"""

import os
import yaml

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "config.yaml",
)


def load_config():
    with open(_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


CONFIG = load_config()
