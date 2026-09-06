"""
# clsproperties
- **Version:** [1.0.0](https://github.com/icb08/clsproperties/releases/tag/v1.0.0) ([Python 3.6+](https://www.python.org/downloads/))
- **Author:** [Isaac Bell](https://github.com/icb08)
- **License:** [MIT](https://github.com/icb08/clsproperties/blob/main/LICENSE)

This library provides `classproperty` objects for controlled access to class attributes.

The `classproperty` class aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable. Like `property` objects, `classproperty` objects are descriptors, supporting getter, setter and deleter functions. 

## Links

### [Documentation](https://icb08.github.io/clsproperties/v1.0.0/documentation)

> This is the GitHub Pages site containing the full documentation for the `clsproperties` library. All guides, examples and references for the installation and implementation of the library are documented here.

### [Repository](https://github.com/icb08/clsproperties)

> This is the GitHub Repository containing the source code for the `clsproperties` library. All source directories and files of the library, and their entire commit history are documented here.

### [Releases](https://github.com/icb08/clsproperties/releases)

> This is the GitHub Releases Page (changelog) for the `clsproperties` library. All source files, distribution files, and release notes, for major, minor and patch releases of the library, are documented here.

---

## Contribution

This library is a solo project, developed and maintained by a student, for the purpose of learning Python and the software development environment.

As an open source project, any community contributions are greatly appreciated! Please always be respectful towards others and the project.

Keep in mind that it may take some time for issues and pull requests to be reviewed, and that some requests may be denied due to the strict code and documentation standards I have set for myself. Also, please try to use official issue templates.

### [Issues](https://github.com/icb08/clsproperties/issues)

> This is the GitHub Issues Page (bug tracker) for the `clsproperties` library. Any feedback (problems / suggestions) or questions about the library can be sent here.

### [Pull Requests](https://github.com/icb08/clsproperties/pulls)

> This is the GitHub Pull Requests Page for the `clsproperties` library. Any code suggestions for the library can be sent here.
"""

__author__ = "Isaac Bell"
__version__ = "1.0.0"
__all__ = ["classproperty", "ClassPropertyMeta"]

class classproperty:
    """
    Class property object.

    This class defines a `classproperty` descriptor, supporting getter, setter and deleter functions, that aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable.

    For detailed information on usage and implementation, view the [Documentation](https://icb08.github.io/clsproperties/v1.0.0/reference/classes.md#classproperty).

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
    """

    def __init__(self, fget: function = None, fset: function = None, fdel: function = None, doc: str = None):
        """
        Instantiate a `classproperty` object.

        This method instantiates a `classproperty` descriptor, defining the getter, setter and deleter functions.

        For detailed information on usage and implementation, view the [Documentation](https://icb08.github.io/clsproperties/v1.0.0/reference/classes.md#classproperty).
        
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
        self.fget = fget.__func__ if isinstance(fget, (classmethod, staticmethod)) else fget
        self.fset = fset.__func__ if isinstance(fset, (classmethod, staticmethod)) else fset
        self.fdel = fdel.__func__ if isinstance(fdel, (classmethod, staticmethod)) else fdel
        self.__doc__ = doc or (self.fget.__doc__ if self.fget else None)

    def __set_name__(self,  cls,  name):
        self.__name__ = name
    
    def __get__(self,  instance,  cls=None):
        if cls is None: cls = type(instance)
        if self.fget is None: raise AttributeError(f"Class property '{self.__name__}' of '{cls.__name__}' object has no getter.")
        return self.fget(cls)
    
    def __set__(self,  instance,  value):
        cls = type(instance)
        if self.fset is None: raise AttributeError(f"Class property '{self.__name__}' of '{cls.__name__}' object has no setter.")
        return self.fset(cls, value)
    
    def __delete__(self,  instance):
        cls = type(instance)
        if self.fdel is None: raise AttributeError(f"Class property '{self.__name__}' of '{cls.__name__}' object has no deleter.")
        return self.fdel(cls)
    
    def getter(self,  fget):
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
        return type(self)(fget,  self.fset,  self.fdel,  self.__doc__)
    
    def setter(self,  fset):
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
        return type(self)(self.fget,  fset,  self.fdel,  self.__doc__)
    
    def deleter(self,  fdel):
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
        return type(self)(self.fget,  self.fset,  fdel,  self.__doc__)
    
class ClassPropertyMeta(type):
    """
    Class property metaclass.

    This class defines a metaclass, that enables full functionality of `classproperty` objects defined in classes, whose metaclass is `ClassPropertyMeta`. This metaclass intercepts class attribute assignment and deletion operations of `classproperty` objects, and executes the corresponding setter and deleter functions of the `classproperty` objects.
    
    For detailed information on usage and implementation, view the [Documentation](https://icb08.github.io/clsproperties/v1.0.0/reference/classes.md#classpropertymeta).

    ---

    ## Attributes / Properties
    N/A

    ---

    ## Methods / Functions
    N/A
    """

    def __setattr__(cls,  name,  value):
        attr = cls.__dict__.get(name)
        if isinstance(attr,  classproperty):
            if attr.fset is None: raise AttributeError(f"Class property '{name}' of '{cls}' object has no setter.")
            return attr.fset(cls, value)
        super().__setattr__(name, value)

    def __delattr__(cls, name):
        attr = cls.__dict__.get(name)
        if isinstance(attr, classproperty):
            if attr.fdel is None: raise AttributeError(f"Class property '{name}' of '{cls}' object has no deleter.")
            return attr.fdel(cls)
        super().__delattr__(name)
