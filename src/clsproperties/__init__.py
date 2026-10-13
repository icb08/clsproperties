"""
PASTE README
"""

# Defines module dunder attributes specifying library metadata and the public API for wildcard imports of the clsproperties library.
__version__ = "1.0.0"
__author__ = "Isaac Bell"
__license__ = "MIT"
__all__ = ["classproperty", "ClassPropertyMeta"]

# Imports custom Python modules, exposing the public API.
from .core import classproperty, ClassPropertyMeta
from . import true