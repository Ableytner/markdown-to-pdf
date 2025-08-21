"""
Pytest fixtures
"""

import os
import shutil

import pytest

from abllib import fs, log

# pylint: disable=protected-access, missing-class-docstring

logger = log.get_logger("test")

@pytest.fixture(scope="session", autouse=True)
def setup():
    """Setup the PersistentStorage, VolatileStorage and StorageView for test usage"""

    # setup testing dirs
    TESTING_DIR = fs.absolute(os.path.dirname(__file__), "..", "..", "test_run")
    shutil.rmtree(TESTING_DIR, ignore_errors=True)
    os.makedirs(TESTING_DIR, exist_ok=True)
    os.chdir(TESTING_DIR)

    #  setup logging
    log.initialize(log.LogLevel.DEBUG)
    log.add_console_handler()

    yield None

@pytest.fixture(scope="function", autouse=False)
def capture_logs():
    """Save all log output to a new file test.log in the root dir"""

    log.initialize(log.LogLevel.DEBUG)
    log.add_file_handler("test.log")

    yield None

    log.initialize()
    log.add_console_handler()
    # file is created lazily
    if os.path.isfile("test.log"):
        os.remove("test.log")
