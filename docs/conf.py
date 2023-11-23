# Configuration file for the Sphinx documentation builder.

project = "SOX"
copyright = "2023, Ali Hemmatifar"
author = "Ali Hemmatifar"


# General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    # "myst_parser",
    "myst_nb",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Options for HTML output

html_theme = "furo"
html_static_path = ["_static"]


# Options for correct display of Plotly in myst_nb

html_js_files = ["https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"]
