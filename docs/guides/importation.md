# Importation

Once installed, to use this library, it must be imported. By importing the library, you put the objects provided by the library into your script's namespace dictionary so they can be accessed in your script. This library provides just 2 objects: the `classproperty` and `ClassPropertyMeta` classes (see the [Classes Reference](../references/classes.md)). There are 3 ways to import the library: Standard, Specific or Wildcard Importation.

See more information on importing Python Modules [here](https://docs.python.org/3/tutorial/modules.html).

> [!NOTE]
> 
> Skip to the relevant section:
> 
> - [Standard Importation](#standard-importation)
> - [Specific Importation](#specific-importation)
> - [Wildcard Importation](#wildcard-importation)

---

## Standard Importation

This method imports the entire library, however you must prefix all objects with `clsproperties`. This is because you import the entire library as a module object called `clsproperties`, which is then added to the script's namespace, and all objects are imported as attributes of the `clsproperties` module object.

To use a standard import, add the following line to the top of your script:

```python
import clsproperties
```

To use the library with a standard import, you must prefix the `classproperty` and `ClassPropertyMeta` classes with `clsproperties`:

```python
import clsproperties

class ExampleClass(metaclass=clsproperties.ClassPropertyMeta):
    _example_value = 67

    @clsproperties.classproperty
    def example_value(cls):
        return _example_value
```

```console
>>> print(ExampleClass.example_value)
67
```

> [!TIP]
> 
> You should use this method if:
> 
> - You want to keep your imports minimal.
> - You don't want to clutter the module's namespace with lots of identifiers (especially if your module is to be imported elsewhere).
> - You want to track the external library where each class comes from.

## Specific Importation

This method imports only selected objects, without any prefixes. This is because you import the selected objects individually, which are then added to the script's namespace, as opposed to importing them as attributes of a module object.

To use a specific import, add the following line to the top of your script:

```python
from clsproperties import classproperty, ClassPropertyMeta
```

To use the library with a specific import, you have to state which objects you would like to import in the import statement, but don't have to prefix any classes:

```python
from clsproperties import classproperty, ClassPropertyMeta

class ExampleClass(metaclass=ClassPropertyMeta):
    _example_value = 67

    @classproperty
    def example_value(cls):
        return _example_value
```

```console
>>> print(ExampleClass.example_value)
67
```

> [!TIP]
> 
> You should use this method if:
> 
> - You want to control which classes you import.
> - You don't want to clutter your code with prefixes (emulating Python's built-in property object better).

## Wildcard Importation

This method imports the entire library, without any prefixes. This is because you import all of the objects individually, which are then added to the script's namespace, as opposed to importing them all as attributes of a module object.

To use a wildcard import, add the following line to the top of your script:

```python
from clsproperties import *
```

To use this library with a wildcard import, you don't have to state which objects you would like to import (as you import them all), and you don't have to prefix any classes:

```python
from clsproperties import *

class ExampleClass(metaclass=ClassPropertyMeta):
    _example_value = 67

    @classproperty
    def example_value(cls):
        return _example_value
```

```console
>>> print(ExampleClass.example_value)
67
```

> [!TIP]
> 
> You should use this method if:
> 
> - You want to easily import the entire library, without cluttering your code with prefixes (emulating Python's built-in property object better).

> [!WARNING]
> 
> It is generally not recommended to do wildcard imports, unless you are aware of everything they import, as it can clutter your script's namespace and accidentally overwrite existing variables or functions.
> 
> In this case, it should be fine, as the only objects imported are the `classproperty` and `ClassPropertyMeta` classes (see the [Classes Reference](../references/classes.md)).
