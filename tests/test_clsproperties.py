import pytest
from clsproperties import classproperty, ClassPropertyMeta

class TestClassProperty:

    def test_empty(self):

        class ExampleClass:
            value_callable = classproperty()

        example_instance = ExampleClass()

        with pytest.raises(AttributeError):
            example_instance.value_callable

        with pytest.raises(AttributeError):
            ExampleClass.value_callable

        with pytest.raises(AttributeError):
            example_instance.value_callable = "new value"

        ExampleClass.value_callable = "new value"
        assert example_instance.value_callable == "new value"
        assert ExampleClass.value_callable == "new value"
