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
import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme
from recommonmark.transform import AutoStructify
# -- Project information -----------------------------------------------------

project = 'Vela'
copyright = 'iot.mi.com/vela'
author = 'xiaomi.com'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.todo",
    "sphinx_tabs.tabs",
    "sphinx_markdown_tables",
    'myst_parser',
    'breathe',
]

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

html_theme = "furo"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    'style_nav_header_background': 'black',
    'collapse_navigation' : False,
    'titles_only': True,
}
html_title = "Xiaomi Vela"
html_show_sphinx = False
html_show_sourcelink = False
html_domain_indices = False
html_last_updated_fmt = "%b %d, %Y"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_favicon = "_static/logo/openvela.svg"
language = 'en'
highlight_language = 'c'
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

build_type = os.getenv('type')
print("生成文档类型为:", build_type)
if build_type is None:
    build_type = 'full'
if build_type == 'trunk':
    build_type = 'full'
if build_type == 'openvela':
    build_type = 'public'
os.system("doxygen Doxyfile.{}".format(build_type))
breathe_projects = { 'doxygen': 'doxygen/xml' }

def setup(app):
    app.add_config_value('recommonmark_config', {
            'enable_eval_rst': True,
            'enable_auto_toc_tree': 'True',
            }, True)
    app.add_transform(AutoStructify)
