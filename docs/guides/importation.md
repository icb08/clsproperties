# Importation

Once installed, to use this library, it must be imported. This can be done in 3 ways: Standard, Specific or Wildcard Importation.

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

This method imports the entire library, however you must prefix the `classproperty` and `ClassPropertyMeta` classes with `clsproperties`.

To use a standard import, add the following line to the top of your script:

```python
import clsproperties
```

To use the library with a standard import, you must prefix the `classproperty` and `ClassPropertyMeta` classes with `clsproperties`:

```python
import clsproperties

class ExampleClass(metaclass=clsproperties.MetaClassProperty):
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

This method imports only objects you select, without any prefixing.

To use a specific import, add the following line to the top of your script:

```python
from clsproperties import classproperty, ClassPropertyMeta
```

The clsproperties library comes with 2 classes: `classproperty` and `ClassPropertyMeta` (see the [Classes Reference](../references/classes.md)). The above code imports both classes. To import just 1 of the 2 classes, replace `classproperty, ClassPropertyMeta` with just `classproperty` or just `ClassPropertyMeta`.

To use the library with a specific import, you don't have to prefix any classes with `clsproperties`:

```python
import clsproperties

class ExampleClass(metaclass=MetaClassProperty):
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

