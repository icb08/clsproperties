---
name: Bug Report
about: Report any problems to help us fix the library!
title: ''
labels: bug
assignees: icb08
type: Bug

---

## Python Version
What Python version did this bug occur on?
e.g. 3.6.15

## Bug Description
A clear and concise description of what the problem is.
e.g. When calling class properties via an instance, the getter function isn't executing.

## Steps To Reproduce
A simple step-by-step guide on how to reproduce the bug.
e.g. Install clsproperties, import clsproperties, create a class called TestClass, inside the class create a classmethod called get_classproperty that returns the string "test" and initialise a classproperty object called classprop_name with the fget argument set to get_classproperty, then create an instance of TestClass and print TestClass.classprop_name.

## Expected Behaviour
A clear and concise description of what you would expect to happen when completing the previous steps, if the library was working correctly.
e.g. The get_classproperty method should execute and return "test", which is then printed to the console.

## Actual Behaviour
A clear and concise description of what actually happens when completing the previous steps.
e.g. An AttributeError is raised: 'ClassName' object has no attribute 'classproperty_name'.

## Screenshots
If applicable, add screenshots to help explain the problem.

## Additional Information
If applicable, add any additional information that could be useful.
