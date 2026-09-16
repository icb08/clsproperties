"""
Core implementation of the `clsproperties` library.

FINISH
"""

# Defines a module dunder attribute specifying the public API for wildcard imports.
__all__ = ["classproperty", "ClassPropertyMeta"]

# Imports built-in Python libraries.
from collections.abc import Callable
from typing import Any, Self, TypeAlias  # TypeAlias required for Python 3.11. For Python 3.12+, use type keyword.

# Defines a helper function to get a classproperty descriptor from an object's attribute lookup process.
def _get_classproperty(obj: object, name: str) -> classproperty | None:
    cls = obj if isinstance(obj, type) else type(obj)
    for base in cls.__mro__:
        if name in base.__dict__:
            attr = base.__dict__[name]
            return attr if isinstance(attr, classproperty) else None
    return None

class _OverrideMeta(type):
    ...

# Defines the classproperty class.
class classproperty(metaclass=_OverrideMeta):
    """
    Class property object.

    This class defines a `classproperty` descriptor, supporting getter, setter and deleter functions, that aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable.

    For detailed information on usage and implementation, view the [Documentation](https://icb08.github.io/clsproperties/v{__version__}/reference/classes/classproperty/).

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

    # Defines a helper inner class that creates a reference/handler object for modifying classproperty descriptors.
    class _Reference:

        def __init__(self, obj: object, name: str):
            self._obj: object = obj
            self._class: type[Any] = obj if isinstance(obj, type) else type(obj)
            self._name: str = name
            _classproperty: classproperty | None = _get_classproperty(obj, name)
            if isinstance(_classproperty, classproperty): self._classproperty: classproperty = _classproperty
            else: raise AttributeError(f"object '{obj}' has no classproperty '{name}'.")
    
        def get(self) -> classproperty:
            return self._classproperty
    
        def set(self, value: Any, *, replace_inherited: bool = False) -> None:
            type.__setattr__(self._classproperty.__owner__ if replace_inherited else self._class, self._name, value)
    
        def delete(self) -> None:
            type.__delattr__(self._classproperty.__owner__, self._name)
    
        def getter(self, fget):
            pass

    # Defines a helper inner class that creates an override object for interacting with the override API.
    class _Override:

        def __init__(self):
            self.__doc__ = """Override Functionality"""
    
        def __call__(self, obj: object, name: str) -> classproperty._Reference:
            return classproperty._Reference(obj, name)

        @staticmethod
        def get(obj: object, name: str) -> classproperty | None:
            return classproperty._Reference(obj, name).get()

    __owner__: type[Any]
    __name__: str
    _ClassPropertyGetMethod: TypeAlias = Callable[[type[Any]], Any] | classmethod | staticmethod  # TypeAlias required for Python 3.11. For Python 3.12+, use type keyword. For Python 3.13+, use classmethod[Any, Any] and staticmethod[Any].
    
    def __init__(self, fget: Callable[..., Any] | None = None, fset: Callable[..., Any] | None = None, fdel: Callable[..., Any] | None = None, doc: str | None = None) -> None:
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
        self._statics: dict[str, bool] = {"get": isinstance(fget, staticmethod), "set": isinstance(fset, staticmethod), "delete": isinstance(fdel, staticmethod)}
        self._fget: Callable[[type[Any]],Any] | classmethod | staticmethod | None = fget
        self.fget = fget.__func__ if isinstance(fget, (classmethod, staticmethod)) else fget
        self.fset = fset.__func__ if isinstance(fset, (classmethod, staticmethod)) else fset
        self.fdel = fdel.__func__ if isinstance(fdel, (classmethod, staticmethod)) else fdel
        self.__doc__ = doc or (self.fget.__doc__ if self.fget else None)

    def __set_name__(self, owner: type[Any], name: str) -> None:
        self.__owner__ = owner
        self.__name__ = name
    
    def __get__(self, instance: object | None, cls: type[Any]) -> Any:
        if self.fget is None: raise AttributeError(f"classproperty '{self.__name__}' of class '{cls.__name__}'{' ' if cls is self.__owner__ else f' (inherited from class \'{self.__owner__.__name__}\') '}has no getter.")
        return self.fget(cls)
    
    def __set__(self, obj: object, value: Any) -> None:
        cls = obj if isinstance(obj, type) else type(obj)
        if self.fset is None: raise AttributeError(f"classproperty '{self.__name__}' of class '{cls.__name__}'{' ' if cls is self.__owner__ else f' (inherited from class \'{self.__owner__.__name__}\') '}has no setter.")
        self.fset(cls, value)
    
    def __delete__(self, obj: object) -> None:
        cls = obj if isinstance(obj, type) else type(obj)
        if self.fdel is None: raise AttributeError(f"classproperty '{self.__name__}' of class '{cls.__name__}'{' ' if cls is self.__owner__ else f' (inherited from class \'{self.__owner__.__name__}\') '}has no deleter.")
        self.fdel(cls)
    
    def getter(self, fget: Callable[..., Any]) -> Self:
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
        #fget = 
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset: Callable[..., Any]) -> Self:
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
    
    def deleter(self, fdel: Callable[..., Any]) -> Self:
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

def _override(cls):
    """
    Override Functionality.
    """
    return cls._Override()
type.__setattr__(classproperty, "override", classproperty(_override))