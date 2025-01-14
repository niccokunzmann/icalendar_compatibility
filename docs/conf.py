# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import datetime
import os

on_rtd = os.environ.get("READTHEDOCS", None) == "True"

try:
    import sphinx_rtd_theme

    html_theme = "sphinx_rtd_theme"
    # html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
except ImportError:
    html_theme = "default"
    if not on_rtd:
        print("-" * 74)
        print("Warning: sphinx-rtd-theme not installed, building with default theme.")
        print("-" * 74)

source_suffix = ".rst"
master_doc = "index"

project = "icalendar_compatibility"
this_year = datetime.date.today().year
copyright = f"{this_year}, Nicco Kunzmann"
author = "Nicco Kunzmann"
release = "v0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "icalendar": ("https://icalendar.readthedocs.io/en/latest/", None),
}

templates_path = ["_templates"]

exclude_patterns = ["_build", "lib", "bin", "include", "local"]
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
