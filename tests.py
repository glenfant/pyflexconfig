import json
import logging
import os
import pathlib
from types import SimpleNamespace

import pytest

from pyflexconfig import bootstrap, keep_upper_names

TESTS_DATA_DIR = pathlib.Path(__file__).resolve().parent / "testdata"

DEFAULT_SETTINGS_1_PY = TESTS_DATA_DIR / "defaults_1.py"
CUSTOM_SETTINGS_1_PY = TESTS_DATA_DIR / "custom_1.py"
DEFAULT_SETTINGS_1_JSON = TESTS_DATA_DIR / "defaults_1.json"


def test_keep_upper_names():
    ns = SimpleNamespace(bad=0, _BAD=0, GOOD=0)
    keep_upper_names(ns)
    ns_as_dict = vars(ns)
    assert ns_as_dict == {"GOOD": 0}


def test_no_config():
    config = SimpleNamespace()
    bootstrap(config)
    assert vars(config) == {}


def test_only_defaults():
    config = SimpleNamespace()
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY)
    conf_as_dict = vars(config)
    assert conf_as_dict == {"ONE": 1, "TWO": 2, "THREE": 3}


def test_only_defaults_wo_filter():
    config = SimpleNamespace()
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY, filter_=None)
    conf_as_dict = vars(config)
    assert conf_as_dict == {"ONE": 1, "TWO": 2, "THREE": 3, "ignored_1": None, "_IGNORED_2": None}


def test_hardcoded_option():
    config = SimpleNamespace(HARDCODED=1, ONE=0)
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY)
    # Hardcoded option is preserved (not overriden) because there's no HARDCODED global in defaults config.
    assert config.HARDCODED == 1

    # Hardcoded option overriden (there is a ONE global in the defaults config file)
    assert config.ONE == 1


def test_custom_missing(caplog):
    config = SimpleNamespace()
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY, custom_path="no_such_file.py")

    # It emitted an error message
    assert "Custom config file no_such_file.py does not exist. Ignoring it..." in caplog.messages

    # But provides the default config
    assert config.TWO == 2


def test_custom_config(caplog):
    caplog.set_level(logging.DEBUG)
    config = SimpleNamespace()
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY, custom_path=CUSTOM_SETTINGS_1_PY)

    # We loaded the custom config
    assert f"Will load custom config file {CUSTOM_SETTINGS_1_PY}" in caplog.messages

    # We merged both default and custom configs
    all_option_names = set(vars(config))
    assert all_option_names == {'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE'}

    # THREE overriden
    assert config.THREE == 4


def test_custom_from_envvar(caplog):
    os.environ["CUSTOM_CONFIG_FILE"] = str(CUSTOM_SETTINGS_1_PY)
    caplog.set_level(logging.DEBUG)
    config = SimpleNamespace()
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY, custom_path_envvar="CUSTOM_CONFIG_FILE")

    # We loaded the custom config
    assert f"Will load custom config file {CUSTOM_SETTINGS_1_PY}" in caplog.messages

    # We merged both default and custom configs
    all_option_names = set(vars(config))
    assert all_option_names == {'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE'}

    # THREE overriden
    assert config.THREE == 4


def test_custom_parser():
    def json_parser(path):
        with open(path, "rb") as json_stream:
            return json.load(json_stream)

    config = SimpleNamespace()
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_JSON, parser=json_parser)
    conf_as_dict = vars(config)
    assert conf_as_dict == {"ONE": 1, "TWO": 2, "THREE": 3}


def test_failing_validator():
    def one_must_be_greater_than_two(config):
        """Stupid validator"""
        if not config.ONE > 2:
            raise ValueError("ONE must be > 2 :-)")

    config = SimpleNamespace()
    with pytest.raises(ValueError):
        bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY, validator=one_must_be_greater_than_two)
