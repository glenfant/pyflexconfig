# pyflexconfig

------------

- You prefer using direct Python files to provide configuration data to your Python application,
  just because you can provide any object type you'd prefer in your configuration file.

- You want to place your custom configuration file anywhere you'd prefer, in traditional places like
  `/etc` or wherever you prefer.

- You want your app to provide some default values to some or all configuration data.

- But you may prefer something else than Python files (YAML, JSON, XML, etc.), just provide your own
  parser.

`pyflexconfig` is just another kid in the block in the settings / options / configuration data
management game that fulfills these requirements.

## Features

- Provide the default configuration programmatically, with a default file in your package or through
  environment variables.

- Override the default configuration options with a custom configuration file. You can override one,
  two or all default configuration options.

- You don't like Python configuration files for onr reason or another, even when executed in a
  sandbox. Okay, provide your own parser.
  
- The configuration container is just a global object on which you can add attributes. I recommend
  using a `types.SimpleNamespace` object but anything may do the job.

- You may provide the custom configuration file either through conventional places
  (ie. `/etc/my_custom_config.py`), explicitly through a dedicated command line option, or through an
  environment variable.

- The default filter keeps only UPPERCASED options not starting with an underscore. This allows to
  use temporary variables with lowercase names in your configuration files, that are not exposed in
  the resulting configuration object. You may provide your own filter if you want other rules or add
  other rules to the default one.

- You may finally provide a validator if you need to check the type / value of some or all
  configuration options.

## Installation

### Using pyflexconfig

`pyflexconfig` requires Python 3.6 or later. Install it with the usual pip dance :

```console
pip install pyflexconfig
```

Note that `pyflexconfig` runs on any operating system and does not require packages outside the
stdlib.

### Develop on a fork of pyflexconfig

Of course, provide and activate a dedicated virtual environment with python 3.6 or later, fork
`pyflexconfig`, then:

```console
git clone <your fork URL>
cd pyflexconfig
pip install -e .[dev]
```

Please work from the `develop` branch that supposed to include the latest validated developments.

Please rebase your fork on the `develop` branch and fix the unit tests (run `pytest`) before issuing
a pull / merge request on the `develop` branch of the original Git repository.

Ah ! And of course file an issue that explains your changes.

## Using pyflexconfig

A basic usage :

Your default config file `defaultsettings.py`:

```python
# Warning: do not import here somethong that's not in the stdlib
ONE = 1
TWO = 2
# ...
```

The `settings.py` module in the same directory:

```python
import pathlib
from types import SimpleNamespace
from pyflexconfig import bootstrap

config = SimpleNamespace(
    # "hardcoded" default options
    THREE = 3,
    # ...
)

# Load the default config that ships in the package
_default_config_path = pathlib.Path(__file__).resolve().parent / "defaultsettings.py"
bootstrap(config, default_path=_default_config_path)
```

And your main application:

```python
from .settings import config

def main():
    print(config.ONE)
    print(config.TWO)
    print(config.THREE)

if __name__ == "__main__":
    main()
```

For more examples, please browse the
[demo/](https://github.com/glenfant/pyflexconfig/tree/master/demos) directory of the repository
as well as the [tests.py](https://github.com/glenfant/pyflexconfig/blob/master/tests.py) module.

View the full API issuing in the console:

```console
python -c "import pyflexconfig; help(pyflexconfig)"
```

## License

This software is provided under the terms of the MIT license. See the `LICENSE` file in the Git
repository or [here](https://en.wikipedia.org/wiki/MIT_License).

## Author

This software comes from [Gilles Lenfant](mailto:gilles.lenfant@gmail.com)'s damaged brain.

The development of `pyflexconfig` is sponsored by the [Caisse des
Depots](https://www.caissedesdepots.fr/).  

## Links

- [Github](https://github.com/glenfant/pyflexconfig/)
- [Issues tracker](https://github.com/glenfant/pyflexconfig/issues)
