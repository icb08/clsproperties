# clsproperties
- **Version:** [1.0.0](https://github.com/icb08/clsproperties/releases/tag/v1.0.0) ([Python 3.6+](https://www.python.org/downloads/))
- **Author:** [Isaac Bell](https://github.com/icb08)
- **License:** [MIT](LICENSE.txt)

This library provides `classproperty` objects for controlled access to class attributes.

The `classproperty` class aims to emulate the behaviours of Python's built-in `property` class, providing controlled access to class attributes instead of instance attributes. Like `property` objects, `classproperty` objects support use both as a decorator and as a callable. Like `property` objects, `classproperty` objects are descriptors, supporting getter, setter and deleter functions. 

---

# Links

## [Documentation](docs/index.md)

## [Repository](https://github.com/icb08/clsproperties)

> This is the GitHub Repository containing the source code for the `clsproperties` library. All source folders and files of the library, and their entire commit history are documented here.

## [Releases](https://github.com/icb08/clsproperties/releases)

> This is the GitHub Releases Page (changelog) for the `clsproperties` library. All source files, distribution files, and release notes, for major, minor and patch releases of the library, are documented here.

## [Issues](https://github.com/icb08/clsproperties/issues)

> This is the GitHub Issues Page (bug tracker) for the `clsproperties` library. Any feedback (suggestions / issues / bugs) for the library can be documented here.

---

# Documentation

This is the full documentation for the `clsproperties` library. All details on the installation, importation and implementation of the library will be documented here.

> [!NOTE]
> Skip to the relevant section:
> 
> - **[Installation](#Installation)**
> - **[Importation](#Importation)**
> - **[Implementation](#Implementation)**

---

## Installation

To use this library, it must first be installed.

> [!IMPORTANT]
> 
> ### Requirements
> 
> - **Python 3.6+**
> > To check your Python version, run the following command in the Python console:
> > 
> > <details open><summary>Windows</summary>
> > 
> > ```
> > py --version
> > ```
> > 
> > </details>
> > 
> > <details><summary>Unix / macOS</summary>
> > 
> > ```
> > python3 --version
> > ```
> > 
> > </details>
> > 
> > This library requires Python version 3.6 or later. If you have an older version of Python and want to update it, install a later version [here](https://python.org/).

### Installing clsproperties

To install this library, run the following command in the Python console:

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

### Updating clsproperties
To update an older version of this library, run the following command in the Python console:

<details open><summary>Windows</summary>

```
py -m pip install clsproperties --upgrade
```

</details>

<details><summary>Unix / macOS</summary>

```
python3 -m pip install clsproperties --upgrade
```

</details>

---

## Importation
Once installed, to use this library, it must be imported. This can be done in 3 ways.
