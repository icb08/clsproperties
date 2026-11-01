"""
Advanced / true implementation of the `clsproperties` library.

FINISH
"""

# Defines a module dunder attribute specifying the public API for wildcard imports of the true module.
__all__ = ["classproperty", "ClassPropertyMetaClass"]

# Imports custom Python modules, exposing the public API.
from .core import classproperty, ClassPropertyMetaClass