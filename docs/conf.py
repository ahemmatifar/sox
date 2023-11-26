# Configuration file for the Sphinx documentation builder.

project = "SOX"
copyright = "2023, Ali Hemmatifar"
author = "Ali Hemmatifar"


# General configuration

extensions = [
    "sphinx.ext.duration",  # for timing the build
    # "sphinx.ext.autosectionlabel",  # for referencing sections
    # "sphinx.ext.autodoc",  # for generating docs from docstrings
    "sphinx.ext.napoleon",  # for parsing numpy-style docstrings
    "autoapi.extension",  # for generating API docs from docstrings
    "myst_nb",  # this replaces myst_parser and allows us to use jupyter notebooks
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Options for HTML output

html_theme = "furo"
html_static_path = ["_static"]


# Options for napoleon

napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Options for myst-nb

myst_enable_extensions = [
    "dollarmath",  # for inline math
]

# Options for autoapi

autodoc_typehints = "signature"  # include type hints in the signature
autoapi_dirs = ["../src"]  # path to the source code
autoapi_type = "python"  # type of source code
autoapi_add_toctree_entry = True  # adds a toctree entry for each module
autoapi_options = [
    "members",  # include members
    "undoc-members",  # include members without docstrings
    "show-inheritance",  # include inheritance
    "show-module-summary",  # include module summary
    # "show-inheritance-diagram",  # include inheritance diagrams
]
