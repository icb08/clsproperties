"""
Basic implementation of the `clsproperties` library.

FINISH
"""

from __future__ import annotations # Required for Python 3.11 - 3.13. For Python 3.14+, built-in. Enables lazy annotations (type hints are evaluated as strings at compile time until runtime, allowing for forward references with circular dependencies).

# Defines a module dunder attribute specifying the public API for wildcard imports.
__all__ = ["classproperty", "ClassPropertyMeta"]

# Imports built-in Python libraries.
from collections.abc import Callable
from typing import Any, Self, TypeAlias  # TypeAlias required for Python 3.11. For Python 3.12+, use type keyword.

# Defines types for type hinting - TypeAlias required for Python 3.11. For Python 3.12+, use type keyword.
_ClassPropertyGetMethod: TypeAlias = Callable[[type[Any]], Any] | classmethod | staticmethod
_ClassPropertySetMethod: TypeAlias = Callable[[type[Any], Any], None] | classmethod | staticmethod
_ClassPropertyDelMethod: TypeAlias = Callable[[type[Any]], None] | classmethod | staticmethod

# Defines a helper function to get a classproperty descriptor from an object's attribute lookup process. FINISH
def _get_classproperty(obj: object, name: str) -> classproperty | None:
    cls = obj if isinstance(obj, type) else type(obj)
    for base in cls.__mro__:
        if name in base.__dict__:
            attr = base.__dict__[name]
            return attr if isinstance(attr, classproperty) else None
    return None

# Defines a helper metaclass for the classproperty class. FINISH
class _Meta(type):

    @property
    def override(cls) -> _Override:
        """
        Override Functionality.

        FINISH
        """
        return _Override()

    @property
    def update(cls) -> _Update:
        """
        Update Functionality.

        FINISH
        """
        return _Update()

# Defines the classproperty class.
class classproperty(metaclass=_Meta):
    """
    Class property object.

    This class defines a `classproperty` descriptor, supporting getter, setter and deleter functions, that aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable.

    For detailed information on usage and implementation, view the [Documentation](https://icb08.github.io/clsproperties/v1.0.0/reference/classes/classproperty/).

    ---

    ## Attributes / Properties
    - **fget** (property) : *callable* | None
    > The getter function of the `classproperty` object.
    - **fset** (property) : *callable* | None
    > The setter function of the `classproperty` object.
    - **fdel** (property) : *callable* | None
    > The deleter function of the `classproperty` object.

    ---

    ## Methods / Functions
    - **getter** (instance method)
    > Define the getter function of the `classproperty` object.
    - **setter** (instance method)
    > Define the setter function of the `classproperty` object.
    - **deleter** (instance method)
    > Define the deleter function of the `classproperty` object.
    """
    
    def __init__(self, fget: _ClassPropertyGetMethod | None = None, fset: _ClassPropertySetMethod | None = None, fdel: _ClassPropertyDelMethod | None = None, doc: str | None = None) -> None:
        """
        Instantiate a `classproperty` object.

        This method instantiates a `classproperty` descriptor, defining the getter, setter and deleter functions.

        For detailed information on usage and implementation, view the [Documentation](https://icb08.github.io/clsproperties/v1.0.0/reference/classes/classproperty/).
        
        ---

        ## Parameters / Arguments
        - **fget** (optional) : *function* (default = None)
        > The getter function of the `classproperty` object.
        - **fset** (optional) : *function* (default = None)
        > The setter function of the `classproperty` object.
        - **fdel** (optional) : *function* (default = None)
        > The deleter function of the `classproperty` object.
        - **doc** (optional) : *str* (default = None)
        > Optional docstring for the `classproperty` object.
        """
        self.fget: _ClassPropertyGetMethod | None = fget
        self.fset: _ClassPropertySetMethod | None = fset
        self.fdel: _ClassPropertyDelMethod | None = fdel
        self.__doc__: str | None = doc if doc is not None else ((self.fget.__func__ if isinstance(self.fget, (classmethod, staticmethod)) else self.fget).__doc__ if self.fget is not None else None)

    def __set_name__(self, owner: type[Any], name: str) -> None:
        self.__owner__: type[Any] = owner
        self.__name__: str = name

    def __get__(self, instance: object | None, cls: type[Any]) -> Any:
        func = self.fget
        if func is None:
            if hasattr(self, "__name__") and hasattr(self, "__owner__"):
                inherited = " " if cls is self.__owner__ else f" (inherited from class '{self.__owner__.__name__}') "
                raise AttributeError(f"classproperty '{self.__name__}' of class '{cls.__name__}'{inherited}has no getter.")
            else:
                raise AttributeError(f"classproperty of class '{cls.__name__}' has no getter.")
        elif isinstance(func, staticmethod): return func.__func__()
        elif isinstance(func, classmethod): return func.__func__(cls)
        else: return func(cls)

    def __set__(self, obj: object, value: Any) -> None:
        cls = obj if isinstance(obj, type) else type(obj)
        func = self.fset
        if func is None:
                    if hasattr(self, "__name__") and hasattr(self, "__owner__"):
                        inherited = " " if cls is self.__owner__ else f" (inherited from class '{self.__owner__.__name__}') "
                        raise AttributeError(f"classproperty '{self.__name__}' of class '{cls.__name__}'{inherited}has no setter.")
                    else:
                        raise AttributeError(f"classproperty of class '{cls.__name__}' has no setter.")
        elif isinstance(func, staticmethod): func.__func__(value)
        elif isinstance(func, classmethod): func.__func__(cls, value)
        else: func(cls, value)
    
    def __delete__(self, obj: object) -> None:
        cls = obj if isinstance(obj, type) else type(obj)
        func = self.fdel
        if func is None:
                    if hasattr(self, "__name__") and hasattr(self, "__owner__"):
                        inherited = " " if cls is self.__owner__ else f" (inherited from class '{self.__owner__.__name__}') "
                        raise AttributeError(f"classproperty '{self.__name__}' of class '{cls.__name__}'{inherited}has no deleter.")
                    else:
                        raise AttributeError(f"classproperty of class '{cls.__name__}' has no deleter.")
        elif isinstance(func, staticmethod): func.__func__()
        elif isinstance(func, classmethod): func.__func__(cls)
        else: func(cls)
    
    def getter(self, fget: _ClassPropertyGetMethod | None) -> Self:
        """
        Define the getter function of the `classproperty` object.

        This method, typically used as a decorator, defines the getter function of the `classproperty` descriptor.

        ---

        ## Parameters / Arguments
        - **fget** : *function*
        > The getter function of the `classproperty` object.

        ---

        ## Returns
        - *`classproperty` object*
        > Returns a new `classproperty` object, with the specified getter function.
        """
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset: _ClassPropertySetMethod | None) -> Self:
        """
        Define the setter function of the `classproperty` object.

        This method, typically used as a decorator, defines the setter function of the `classproperty` descriptor.

        ---

        ## Parameters / Arguments
        - **fset** : *function*
        > The setter function of the `classproperty` object.

        ---

        ## Returns
        - *`classproperty` object*
        > Returns a new `classproperty` object, with the specified setter function.
        """
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
    def deleter(self, fdel: _ClassPropertyDelMethod | None) -> Self:
        """
        Define the deleter function of the `classproperty` object.

        This method, typically used as a decorator, defines the deleter function of the `classproperty` descriptor.

        ---

        ## Parameters / Arguments
        - **fdel** : *function*
        > The deleter function of the `classproperty` object.

        ---

        ## Returns
        - *`classproperty` object*
        > Returns a new `classproperty` object, with the specified deleter function.
        """
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

class ClassPropertyMeta(type):
    """
    Class property metaclass.

    This class defines a metaclass, that enables full functionality of `classproperty` objects defined in classes, whose metaclass is `ClassPropertyMeta`. This metaclass intercepts class attribute assignment and deletion operations of `classproperty` objects, and executes the corresponding setter and deleter functions of the `classproperty` objects.
    
    For detailed information on usage and implementation, view the [Documentation](https://icb08.github.io/clsproperties/v1.0.0/reference/classes/classpropertymeta/).

    ---

    ## Attributes / Properties
    N/A

    ---

    ## Methods / Functions
    N/A
    """

    def __setattr__(cls, name: str, value: Any) -> None:
        attr = _get_classproperty(cls, name)
        if isinstance(attr, classproperty): attr.__set__(cls, value)
        else: super().__setattr__(name, value)

    def __delattr__(cls, name: str) -> None:
        attr = _get_classproperty(cls, name)
        if isinstance(attr, classproperty): attr.__delete__(cls)
        else: super().__delattr__(name)

class _Reference:

    def __init__(self, obj: object, name: str) -> None:
        self._obj: object = obj
        self._class: type[Any] = obj if isinstance(obj, type) else type(obj)
        self._name: str = name
        _classproperty: classproperty | None = _get_classproperty(obj, name)
        if isinstance(_classproperty, classproperty): self._classproperty: classproperty = _classproperty
        else: raise AttributeError(f"object '{obj}' has no classproperty '{name}'.")

class _OverrideReference(_Reference):

    def __init__(self, obj: object, name: str) -> None:
        super().__init__(obj, name)
    
    def get(self) -> classproperty:
        """
        FINISH
        """
        return self._classproperty
    
    def set(self, value: Any, *, replace_inherited: bool = False) -> None:
        """
        FINISH
        """
        type.__setattr__(self._classproperty.__owner__ if replace_inherited else self._class, self._name, value)
    
    def delete(self) -> None:
        """
        FINISH
        """
        type.__delattr__(self._classproperty.__owner__, self._name)

class _Override:
    
    def __call__(self, obj: object, name: str) -> _OverrideReference:
        return _OverrideReference(obj, name)

    @staticmethod
    def get(obj: object, name: str) -> classproperty:
        """
        FINISH
        """
        return _OverrideReference(obj, name).get()

    @staticmethod
    def set(obj: object, name: str, value: Any, *, replace_inherited: bool = False) -> None:
        """
        FINISH
        """
        _OverrideReference(obj, name).set(value, replace_inherited=replace_inherited)

    @staticmethod
    def delete(obj: object, name: str) -> None:
        """
        FINISH
        """
        _OverrideReference(obj, name).delete()

class _UpdateReference(_Reference):

    def __init__(self, obj: object, name: str) -> None:
        super().__init__(obj, name)

    def getter(self, fget: _ClassPropertyGetMethod | None) -> None:
        """
        FINISH
        """
        self._classproperty.fget = fget

    def setter(self, fset: _ClassPropertySetMethod | None) -> None:
        """
        FINISH
        """
        self._classproperty.fset = fset

    def deleter(self, fdel: _ClassPropertyDelMethod | None) -> None:
        """
        FINISH
        """
        self._classproperty.fdel = fdel

    def docstring(self, doc: str | None) -> None:
        """
        FINISH
        """
        self._classproperty.__doc__ = doc

class _Update:

    def __call__(self, obj: object, name: str) -> _UpdateReference:
        return _UpdateReference(obj, name)
    
    @staticmethod
    def getter(obj: object, name: str, fget: _ClassPropertyGetMethod | None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).getter(fget)
    
    @staticmethod
    def setter(obj: object, name: str, fset: _ClassPropertySetMethod | None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).setter(fset)
    
    @staticmethod
    def deleter(obj: object, name: str, fdel: _ClassPropertyDelMethod | None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).deleter(fdel)

    @staticmethod
    def docstring(obj: object, name: str, doc: str | None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).docstring(doc)