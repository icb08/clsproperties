"""
Basic implementation of the `clsproperties` library.

FINISH
"""

# Enables lazy annotations (type hints are evaluated as strings at compile time until runtime, allowing for forward references with circular dependencies) - Required for Python 3.12 - 3.13. For Python 3.14+, built-in.
from __future__ import annotations

# Defines a module dunder attribute specifying the public API for wildcard imports.
__all__ = ["classproperty", "ClassPropertyMetaClass"]

# Imports built-in Python libraries.
from typing import Self, Callable, Any
from types import EllipsisType, MappingProxyType # In Python 3.15+, use _NONE = sentinel("_NONE") for default values, instead of ... (type EllipsisType).

# Defines type aliases that specify the requirements for classproperty accessor methods.
type ClassPropertyGetter[Cls, GetValue] = Callable[[type[Cls]], GetValue] | classmethod[Cls, [], GetValue] | staticmethod[[], GetValue]
type ClassPropertySetter[Cls, SetValue] = Callable[[type[Cls], SetValue], None] | classmethod[Cls, [SetValue], None] | staticmethod[[SetValue], None]
type ClassPropertyDeleter[Cls] = Callable[[type[Cls]], None] | classmethod[Cls, [], None] | staticmethod[[], None]

# Defines a helper function to get a classproperty data descriptor from an object's attribute lookup process.
def _get_classproperty[Cls](obj: type[Cls] | Cls, name: str) -> tuple[classproperty[Cls, Any, Any] | None, type[Any] | None]:
    cls: type[Cls] = obj if isinstance(obj, type) else type(obj)
    mro: tuple[type[Any], ...] = type.__getattribute__(cls, "__mro__")  # Required for no recursion in ClassPropertyMetaClass __getattribute__ method (can't do cls.__mro__).
    for base in mro:
        namespace: MappingProxyType[str, Any] = type.__getattribute__(base, "__dict__")  # Required for no recursion in ClassPropertyMetaClass __getattribute__ method (can't do base.__dict__ if base is cls).
        if name in namespace: return (attr, base) if isinstance((attr:=namespace[name]), classproperty) else (None, None)
    return None, None

# Defines a private metaclass for the classproperty class, that provides access to the override and update functionality via the class.
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

# Defines the classproperty class, that provides controlled access to class attributes.
class classproperty[Cls, GetValue, SetValue](metaclass=_Meta):
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
    
    def __init__(self, fget: ClassPropertyGetter[Cls, GetValue] | None = None, fset: ClassPropertySetter[Cls, SetValue] | None = None, fdel: ClassPropertyDeleter[Cls] | None = None, doc: str | None | EllipsisType = ...) -> None:
        """
        Instantiate a `classproperty` object.

        This method instantiates a `classproperty` descriptor, defining the getter, setter and deleter functions.

        For detailed information on implementation, view the [Documentation](https://icb08.github.io/clsproperties/v1.0.0/reference/classes/classproperty/).
        
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
        self.fget: ClassPropertyGetter[Cls, GetValue] | None = fget
        self.fset: ClassPropertySetter[Cls, SetValue] | None = fset
        self.fdel: ClassPropertyDeleter[Cls] | None = fdel
        fget_func = self._get_function("fget")
        self._get_function("fset")
        self._get_function("fdel")
        self._doc: bool = doc is not ...
        self.__doc__: str | None = doc if doc is not ... else getattr(fget_func, "__doc__", None)

    def __set_name__(self, owner: type[Cls], name: str) -> None:
        self.__owner__: type[Cls] = owner
        self.__name__: str = name

    def __get__(self, instance: Cls | EllipsisType | None, cls: type[Cls]) -> GetValue | Self:
        if instance is None: return self
        func = self._get_function("fget", self.fget)
        if func is None: raise AttributeError(f"classproperty{f" '{self.__name__}' " if hasattr(self, "__name__") else " "}of class '{cls.__name__}'{f" (inherited from class '{self.__owner__.__name__}') " if hasattr(self, "__owner__") and cls is not self.__owner__ else " "}has no getter.")
        elif isinstance(self.fget, staticmethod): return func()
        else: return func(cls)
 
    def __set__(self, obj: Cls | type[Cls], value: SetValue) -> None:
        cls: type[Cls]  = obj if isinstance(obj, type) else type(obj)
        func = self._get_function("fset")
        if func is None: raise AttributeError(f"classproperty{f" '{self.__name__}' " if hasattr(self, "__name__") else " "}of class '{cls.__name__}'{f" (inherited from class '{self.__owner__.__name__}') " if hasattr(self, "__owner__") and cls is not self.__owner__ else " "}has no setter.")
        elif isinstance(self.fset, staticmethod): func(value)
        else: func(cls, value)
    
    def __delete__(self, obj: Cls | type[Cls]) -> None:
        cls: type[Cls] = obj if isinstance(obj, type) else type(obj)
        func = self._get_function("fdel")
        if func is None: raise AttributeError(f"classproperty{f" '{self.__name__}' " if hasattr(self, "__name__") else " "}of class '{cls.__name__}'{f" (inherited from class '{self.__owner__.__name__}') " if hasattr(self, "__owner__") and cls is not self.__owner__ else " "}has no deleter.")
        elif isinstance(self.fdel, staticmethod): func()
        else: func(cls)
    
    def getter(self, fget: ClassPropertyGetter[Cls, GetValue] | None) -> Self:
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
        self._get_function("fget", fget)
        return type(self)(fget, self.fset, self.fdel, self.__doc__ if self._doc else ...)
    
    def setter(self, fset: ClassPropertySetter[Cls, SetValue] | None) -> Self:
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
        self._get_function("fset", fset)
        return type(self)(self.fget, fset, self.fdel, self.__doc__ if self._doc else ...)
    
    def deleter(self, fdel: ClassPropertyDeleter[Cls] | None) -> Self:
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
        self._get_function("fdel", fdel)
        return type(self)(self.fget, self.fset, fdel, self.__doc__ if self._doc else ...)

    def _get_function(self, name: str, method: ClassPropertyGetter[Cls, GetValue] | ClassPropertySetter[Cls, SetValue] | ClassPropertyDeleter[Cls] | None | EllipsisType = ...) -> Callable[..., Any] | None:
        if method is ...: method = getattr(self, name, None)
        if method is None: return None
        elif isinstance(method, (classmethod, staticmethod)): return method.__func__
        elif callable(method): return method
        else: raise TypeError(f"accessor method '{name}' of classproperty{f" '{self.__name__}' " if hasattr(self, "__name__") else " "} must be a callable, classmethod or staticmethod.")

# Defines the ClassPropertyMetaClass metaclass that ensures the setter and deleter accessor methods of classproperty objects execute when accessed via the class.
class ClassPropertyMetaClass(type):
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

    def __getattribute__(cls: type[Any], name: str) -> Any:
        attr = _get_classproperty(cls, name)[0]
        if attr is None: return type.__getattribute__(cls, name)
        else: return attr.__get__(..., cls)

    def __setattr__(cls: type[Any], name: str, value: Any) -> None:
        attr = _get_classproperty(cls, name)[0]
        if attr is None: type.__setattr__(cls, name, value)
        else: attr.__set__(cls, value)

    def __delattr__(cls: type[Any], name: str) -> None:
        attr = _get_classproperty(cls, name)[0]
        if attr is None: type.__delattr__(cls, name)
        else: attr.__delete__(cls)

class _Reference[Cls]:

    def __init__(self, obj: Cls | type[Cls], name: str) -> None:
        self._class: type[Cls] = obj if isinstance(obj, type) else type(obj)
        self._name: str = name
        _classproperty, _owner = _get_classproperty(obj, name)
        if _classproperty is None or _owner is None: raise AttributeError(f"object '{obj}' has no classproperty '{name}'.")
        self._classproperty: classproperty[Cls, Any, Any] = _classproperty
        self._owner: type[Any] = _owner

class _OverrideReference[Cls](_Reference[Cls]):

    def __init__(self, obj: Cls | type[Cls], name: str) -> None:
        super().__init__(obj, name)
    
    def get(self) -> classproperty[Cls, Any, Any]:
        """
        FINISH
        """
        return self._classproperty
    
    def set(self, value: Any, *, replace_inherited: bool = False) -> None:
        """
        FINISH
        """
        type.__setattr__(self._owner if replace_inherited else self._class, self._name, value)
    
    def delete(self) -> None:
        """
        FINISH
        """
        type.__delattr__(self._owner, self._name)

class _Override:

    @staticmethod
    def __call__[Cls](obj: Cls | type[Cls], name: str) -> _OverrideReference[Cls]:
        """
        FINISH
        """
        return _OverrideReference(obj, name)

    @staticmethod
    def get[Cls](obj: Cls | type[Cls], name: str) -> classproperty[Cls, Any, Any]:
        """
        FINISH
        """
        return _OverrideReference(obj, name).get()

    @staticmethod
    def set[Cls](obj: Cls | type[Cls], name: str, value: Any, *, replace_inherited: bool = False) -> None:
        """
        FINISH
        """
        _OverrideReference(obj, name).set(value, replace_inherited=replace_inherited)

    @staticmethod
    def delete[Cls](obj: Cls | type[Cls], name: str) -> None:
        """
        FINISH
        """
        _OverrideReference(obj, name).delete()

class _UpdateReference[Cls](_Reference[Cls]):

    def __init__(self, obj: Cls | type[Cls], name: str) -> None:
        super().__init__(obj, name)

    def getter[GetValue](self, fget: ClassPropertyGetter[Cls, GetValue] | None) -> None:
        """
        FINISH
        """
        func = self._classproperty._get_function("fget", fget)
        doc: str | None = self._classproperty.__doc__ if self._classproperty._doc else func.__doc__
        self._classproperty.fget = fget
        self._classproperty.__doc__ = doc

    def setter[SetValue](self, fset: ClassPropertySetter[Cls, SetValue] | None) -> None:
        """
        FINISH
        """
        self._classproperty._get_function("fset", fset)
        self._classproperty.fset = fset

    def deleter(self, fdel: ClassPropertyDeleter[Cls] | None) -> None:
        """
        FINISH
        """
        self._classproperty._get_function("fdel", fdel)
        self._classproperty.fdel = fdel

    def docstring(self, doc: str | None = None) -> None:
        """
        FINISH
        """
        self._classproperty._doc = True
        self._classproperty.__doc__ = doc

class _Update:

    @staticmethod
    def __call__[Cls](obj: Cls | type[Cls], name: str) -> _UpdateReference[Cls]:
        return _UpdateReference(obj, name)
    
    @staticmethod
    def getter[Cls, GetValue](obj: Cls | type[Cls], name: str, fget: ClassPropertyGetter[Cls, GetValue] | None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).getter(fget)
    
    @staticmethod
    def setter[Cls, SetValue](obj: Cls | type[Cls], name: str, fset: ClassPropertySetter[Cls, SetValue] | None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).setter(fset)
    
    @staticmethod
    def deleter[Cls](obj: Cls | type[Cls], name: str, fdel: ClassPropertyDeleter[Cls] | None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).deleter(fdel)

    @staticmethod
    def docstring[Cls](obj: Cls | type[Cls], name: str, doc: str | None = None) -> None:
        """
        FINISH
        """
        _UpdateReference(obj, name).docstring(doc)