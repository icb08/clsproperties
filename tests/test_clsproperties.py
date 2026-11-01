# Imports built-in Python libraries.
import pytest
# Imports internal packages / modules.
from clsproperties import classproperty, ClassPropertyMetaClass 

class TestClassProperty:

    def test_empty(self):

        class ExampleClass:
            classprop = classproperty()

        example_instance = ExampleClass()

        with pytest.raises(AttributeError): example_instance.classprop
        with pytest.raises(AttributeError): ExampleClass.classprop
        with pytest.raises(AttributeError): example_instance.classprop = "new value"
        with pytest.raises(AttributeError): del example_instance.classprop
        ExampleClass.classprop = "new value"
        assert example_instance.classprop == "new value"
        assert ExampleClass.classprop == "new value"
