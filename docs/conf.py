# Configuration file for the Sphinx documentation builder.

project = "SOX"
copyright = "2023, Ali Hemmatifar"
author = "Ali Hemmatifar"


# General configuration

extensions = [
    "sphinx.ext.duration",  # for timing the build
    "sphinx.ext.autosectionlabel",  # for referencing sections
    "sphinx.ext.autodoc",  # for automatically generating docs from docstrings
    "sphinx.ext.autosummary",  # for automatically generating docs from docstrings
    "myst_nb",  # this replaces myst_parser and allows us to use jupyter notebooks
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Options for HTML output

html_theme = "furo"
html_static_path = ["_static"]


# Options for myst-nb

nb_execution_mode = "off"  # disables notebook execution on build
