"""A CLI tool for subscribed bangumi.

`Project Home <https://github.com/BGmi/BGmi>`_
"""
import os.path

from importlib_metadata import version

from bgmi3 import core

__version__ = version(__package__)
source_root = os.path.dirname(__file__)

__all__ = ["__version__", "core"]
