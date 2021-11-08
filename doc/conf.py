# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import importlib

# -- Project information -----------------------------------------------------

project = 'minecraft-launcher-lib'
copyright = '2019-2021, JakobDev'
author = 'JakobDev'

# The full version, including alpha/beta/rc tags
release = "4.1"

master_doc = 'index'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


def add_optional_extension(name: str):
    try:
        importlib.import_module(name)
        extensions.append(name)
    except ModuleNotFoundError:
        pass


add_optional_extension("sphinx_reredirects")
add_optional_extension("notfound.extension")

redirects = {
    "account": "modules/account.html",
    "command": "modules/command.html",
    "exceptions": "modules/exceptions.html",
    "fabric": "modules/fabric.html",
    "forge": "modules/forge.html",
    "install": "modules/install.html",
    "microsoft_account": "modules/microsoft_account.html",
    "natives": "modules/natives.html",
    "runtime": "modules/runtime.html",
    "utils": "modules/utils.html",
}
