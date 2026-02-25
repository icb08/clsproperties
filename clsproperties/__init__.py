"""
# clsproperties

- **Author:** [Isaac Bell](https://github.com/icb08)
- **Version:** [1.0.0](https://github.com/icb08/clsproperties/wiki/Changelog#1-0-0)

This library provides `classproperty` objects for controlled access to class attributes.

The `classproperty` class aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable. Like `property` objects, `classproperty` objects are descriptors, supporting getter, setter and deleter functions. 

## Links

- **[Source Code](https://github.com/icb08/clsproperties)**
- **[Issues](https://github.com/icb08/clsproperties/issues)**
- **[Documentation](https://github.com/icb08/clsproperties/wiki/Documentation)**
- **[Changelog](https://github.com/icb08/clsproperties/wiki/Changelog)**
- **[License](https://github.com/icb08/clsproperties/blob/main/LICENSE)**
"""

__author__ = "Isaac Bell"
__version__ = "1.0.0"
__all__ = ["classproperty","ClassPropertyMeta"]

class classproperty:
    """
    Class property object.

    This class defines a `classproperty` descriptor, supporting getter, setter and deleter functions, that aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable.

    ---

    ## Attributes / Properties
    - **fget** (attribute) : *function*
    > The getter function of the `classproperty` object.
    - **fset** (attribute) : *function*
    > The setter function of the `classproperty` object.
    - **fdel** (attribute) : *function*
    > The deleter function of the `classproperty` object.

    ---

    ## Methods / Functions
    - **getter** (instance method)
    > Define the getter function of the `classproperty` object.
    - **setter** (instance method)
    > Define the setter function of the `classproperty` object.
    - **deleter** (instance method)
    > Define the deleter function of the `classproperty` object.

    ---

    ## Usage / Implementation
    
    The `classproperty` class aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable.

    In both cases, access to the `classproperty` attribute, via the class itself or via instances of the class, is mediated by the defined getter, setter and deleter functions.

    Important: For the setter and deleter functions to be triggered when the `classproperty` attribute is accessed via the class itself, the `ClassPropertyMeta` class is required.

    For detailed information on usage and implementation, view the [Documentation](https://github.com/icb08/clsproperties/wiki/Documentation).
    
    ### Decorator
    
    Like `property` objects, `classproperty` objects can be defined via a decorator defined on the class.

    Example:

    ```
    class MyClass(metaclass=ClassPropertyMeta):
        
        _value = 67

        @classproperty
        def value(cls):
            return _value
        
        @value.setter
        def value(cls,newvalue):
            cls._value = newvalue
        
    instance = MyClass()

    >>> MyClass.value
    ... 67
    >>> instance.value
    ... 67
    ```

    ### Callable

    Like `property` objects, `classproperty` objects can also be instantiated by passing the getter, setter and deleter functions as arguments.

    Example:

    ```
    class MyClass(metaclass=ClassPropertyMeta):
        
        _value = 67

        def get_value(cls):
            return cls._value
        
        def set_value(cls,newvalue):
            cls._value = newvalue

        value = classproperty(get_value,set_value)
    
    instance = MyClass()

    >>> MyClass.value
    ... 67
    >>> instance.value
    ... 67
    ```
    """

    def __init__(self,fget=None,fset=None,fdel=None,doc=None):
        """Instantiate a `classproperty` object.
        
        """
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or (fget.__doc__ if fget else None)

    def __set_name__(self,cls,name):
        self.__name__ = name
    
    def __get__(self,instance,cls=None):
        if cls is None: cls = type(instance)
        if self.fget is None: raise AttributeError(f"Class property '{self.__name__}' of '{cls.__name__}' object has no getter.")
        return self.fget(cls)
    
    def __set__(self,instance,value):
        cls = type(instance)
        if self.fset is None: raise AttributeError(f"Class property '{self.__name__}' of '{cls.__name__}' object has no setter.")
        return self.fset(cls,value)
    
    def __delete__(self,instance):
        cls = type(instance)
        if self.fdel is None: raise AttributeError(f"Class property '{self.__name__}' of '{cls.__name__}' object has no deleter.")
        return self.fdel(cls)
    
    def getter(self,fget):
        return type(self)(fget,self.fset,self.fdel,self.__doc__)
    
    def setter(self,fset):
        return type(self)(self.fget,fset,self.fdel,self.__doc__)
    
    def deleter(self,fdel):
        return type(self)(self.fget,self.fset,fdel,self.__doc__)
    
class ClassPropertyMeta(type):
    """"""

    def __setattr__(cls,name,value):
        attr = cls.__dict__.get(name)
        if isinstance(attr,classproperty):
            if attr.fset is None: raise AttributeError(f"Class property '{name}' of '{cls}' object has no setter.")
            return attr.fset(cls,value)
        super().__setattr__(name,value)
    
    def __delattr__(cls, name):
        attr = cls.__dict__.get(name)
        if isinstance(attr,classproperty):
            if attr.fdel is None: raise AttributeError(f"Class property '{name}' of '{cls}' object has no deleter.")
            return attr.fdel(cls)
        super().__delattr__(name)
