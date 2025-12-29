# clsproperties

- **Author:** [Isaac Bell](https://github.com/icb08)
- **Version:** [1.0.0](https://github.com/icb08/clsproperties/blob/main/CHANGELOG.md#1-0-0)

This library provides `classproperty` objects for controlled access to class attributes.

The `classproperty` class aims to emulate the behaviours of python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable. Like `property` objects, `classproperty` objects are descriptors, supporting getter, setter and deleter functions. 

---

## Installation

To install this library, run the following command in the python console:

<details open><summary>Windows</summary>
  
```
py -m pip install clsproperties
```

</details>

<details><summary>Unix / macOS</summary>
  
```
python3 -m pip install clsproperties
```

</details>

### Requirements

- **Python 3.6+**

---

## Usage

For detailed information on the usage of this library, view the full documentation [here](https://github.com/icb08/clsproperties/wiki).

### Example Usage

Example 1: Creating a read-only class property.

```py
from clsproperties import classproperty

class ExampleClass:
    _value = "Class Property"

    @classproperty
    def value(cls):
        print("Running Getter")
        return cls._value

exampleinstance = ExampleClass()
```

```
>>> ExampleClass.value
Running Getter

>>> exampleinstance.value
Running Getter
```

Example 2: Creating a class property with a setter and deleter.

```py
from clsproperties import classproperty

class ExampleClass:
    _value = "Class Property"

    @classproperty
    def value(cls):
        print("Running Getter")
        return cls._value

    @value.setter
    def value(cls,new_value):
        print("Running Setter")
        cls._value = new_value

    @value.deleter
    def value(cls):
        print("Running Deleter")
        del cls._value

exampleinstance = ExampleClass()
```

```
>>> ExampleClass.value
Running Getter

>>> exampleinstance.value
Running Getter

>>> ExampleClass.value = "New Class Property"
<Setter NOT run>

>>> exampleinstance.value = "New Class Property"
Running Setter

>>> del ExampleClass.value
<Deleter NOT run>

>>> del exampleinstance.value
Running Deleter
```

Example 3: Creating a class property with a setter and deleter, that works when referenced via the class (instead of overriding the class property, turning the value attribute from a `classproperty` object to a `string` object).

```py
from clsproperties import classproperty,ClassPropertyMeta

class ExampleClass(metaclass=ClassPropertyMeta):
    _value = "Class Property"

    @classproperty
    def value(cls):
        print("Running Getter")
        return cls._value

    @value.setter
    def value(cls,new_value):
        print("Running Setter")
        cls._value = new_value

    @value.deleter
    def value(cls):
        print("Running Deleter")
        del cls._value

exampleinstance = ExampleClass()
```

```
>>> ExampleClass.value
Running Getter

>>> exampleinstance.value
Running Getter

>>> ExampleClass.value = "New Class Property"
Running Setter

>>> exampleinstance.value = "New Class Property"
Running Setter

>>> del ExampleClass.value
Running Deleter

>>> del exampleinstance.value
Running Deleter
```

---

## Links

- **Source:** https://github.com/icb08/clsproperties
- **Documentation:** https://github.com/icb08/clsproperties/wiki
- **Issues:** https://github.com/icb08/clsproperties/issues
- **Changelog:** https://github.com/icb08/clsproperties/blob/main/CHANGELOG.md
- **License:** https://github.com/icb08/clsproperties/blob/main/LICENSE
