import os
import configparser
from typing import Union

from .core import running_as_root

VERSION = '0.8-dev'

if running_as_root():
    CACHE_ROOT = '/var/cache/pikaur'
else:
    CACHE_ROOT = os.path.expanduser('~/.cache/pikaur/')

AUR_REPOS_CACHE_DIR = 'aur_repos'
BUILD_CACHE_DIR = 'build'
PACKAGE_CACHE_DIR = 'pkg'

_CONFIG_ROOT = os.environ.get(
    "XDG_CONFIG_HOME",
    os.path.join(os.environ.get("HOME"), ".config/")
)
CONFIG_PATH = os.path.join(
    _CONFIG_ROOT,
    "pikaur.conf"
)


_CONFIG_SCHEMA = {
    'sync': {
        'AlwaysShowPkgOrigin': {
            'type': 'bool',
            'default': 'no',
        },
    },
    'colors': {
        'Version': {
            'type': 'int',
            'default': '10',
        },
        'VersionDiffOld': {
            'type': 'int',
            'default': '11',
        },
        'VersionDiffNew': {
            'type': 'int',
            'default': '9',
        },
    }
}


_CONFIG_TYPES = Union[str, bool, int]


def write_config(config: configparser.ConfigParser = None) -> None:
    if not config:
        config = configparser.ConfigParser()
    need_write = False
    for section_name, section in _CONFIG_SCHEMA.items():
        if section_name not in config:
            config[section_name] = {}
        for option_name, option_schema in section.items():
            if option_name not in config[section_name]:
                config[section_name][option_name] = option_schema['default']
                need_write = True
    if need_write:
        if not os.path.exists(_CONFIG_ROOT):
            os.makedirs(_CONFIG_ROOT)
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)


class PikaurConfigSection():

    section: configparser.SectionProxy = None

    def __init__(self, section: configparser.SectionProxy) -> None:
        self.section = section

    def get(self, key: str, *args) -> _CONFIG_TYPES:
        section = self.section
        if _CONFIG_SCHEMA[section.name].get(key, {}).get('type') == 'bool':
            return section.getboolean(key)
        if _CONFIG_SCHEMA[section.name].get(key, {}).get('type') == 'int':
            return section.getint(key)
        return section.get(key, *args)


class PikaurConfig():

    _config: configparser.ConfigParser = None

    @classmethod
    def get_config(cls) -> configparser.ConfigParser:
        if not cls._config:
            cls._config = configparser.ConfigParser()
            if not os.path.exists(CONFIG_PATH):
                write_config()
            cls._config.read(CONFIG_PATH)
            write_config(config=cls._config)
        return cls._config

    def __getattr__(self, attr: str) -> PikaurConfigSection:
        return PikaurConfigSection(self.get_config()[attr])

    @classmethod
    def get(cls, section: str, key: str, *args) -> _CONFIG_TYPES:
        return getattr(cls(), section).get(key, *args)
