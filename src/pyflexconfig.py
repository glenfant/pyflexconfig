"""
============
pyflexconfig
============
"""
import logging
import pathlib
import runpy
import types
import typing

import dotenv
import pkg_resources

# Custom logger
LOG = logging.getLogger(name=__name__)

# PEP 396 style version marker
try:
    __version__ = pkg_resources.get_distribution("pyflexconfig").version
except pkg_resources.DistributionNotFound:
    LOG.warning("Could not get the package version from pkg_resources")
    __version__ = "unknown"

__author__ = "Gilles Lenfant"
__author_email__ = "gilles.lenfant@gmail.com"
__license__ = "MIT"

# Typing helpers

PathOrStr = typing.Union[str, pathlib.Path]

def keep_upper_names(config: types.SimpleNamespace) -> None:
    """Remove disallowed option names, the default options filter"""

    def name_rejected(name: str) -> bool:
        """True if not an allowed option name.
        Legal names are:
        - All uppercases with potential "_" or [0..9] inside
        - Don't start with "_"
        """
        return name.startswith("_") or name.upper() != name

    # Remove "illegal" option names.
    for name in vars(config):
        if name_rejected(name):
            delattr(config, name)


def bootstrap(
    config: types.SimpleNamespace,
    defaults_path: typing.Optional[PathOrStr] = None,
    custom_path: typing.Optional[PathOrStr] = None,
    config_file_envvar: str = None,
    filter: typing.Callable = keep_upper_names,
    validator: typing.Optional[typing.Callable] = None,
) -> None:
    """
    Bootstrap the configuration object populating the `config` namespace.

    Args:
        config: The global configuration namespace to populate,

    Kwargs:
        defaults_path: Optional path to the default config file.
        custom_path: Optional
        config_file_envvar: Optional environment variable name that 
        filter_: Optional filtering callable that removes from a config SimpleNamespace unwanted
                 options. Default behaviour is to keep only UPPERCASE options.
        validator: Optional validation callable that takes a config SimpleNamespace and
                   issues warnings or raises exceptions on invalid configuration options.
    
    Note:
        if both ``custom_path`` and ``config_file_envvar`` are provided, the second one is ignored.
    """
    if defaults_path:
        default_options = runpy.run_path()
