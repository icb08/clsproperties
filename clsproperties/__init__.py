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
    """

    def __init__(self,fget=None,fset=None,fdel=None,doc=None):
        """"""
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
