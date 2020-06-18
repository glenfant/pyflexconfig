import logging
import pathlib
from types import SimpleNamespace

from pyflexconfig import bootstrap, keep_upper_names

TESTS_DATA_DIR = pathlib.Path(__file__).resolve().parent / "testdata"

DEFAULT_SETTINGS_1_PY = TESTS_DATA_DIR / "defaults_1.py"
CUSTOM_SETTINGS_1_PY = TESTS_DATA_DIR / "custom_1.py"


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
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY)
    conf_as_dict = vars(config)
    assert conf_as_dict == {"ONE": 1, "TWO": 2, "THREE": 3, "ignored_1": None, "_IGNORED_2": None}


def test_hardcoded_option():
    config = SimpleNamespace(HARDCODED=1, ONE=0)
    bootstrap(config, defaults_path=DEFAULT_SETTINGS_1_PY)
    # Hardcoded option is preserved (not overriden)
    assert config.HARDCODED == 1

    # Hardcoded option overriden
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
