import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'Cogito'
copyright = '2024, Ben Ballintyn'
author = 'Ben Ballintyn'
release = '0.1.2'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
