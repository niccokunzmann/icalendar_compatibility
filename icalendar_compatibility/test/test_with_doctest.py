# icalendar_compatibility
# Copyright (C) 2025  Nicco Kunzmann
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see
# <https://www.gnu.org/licenses/>.
"""This file tests the source code provided by the documentation.

See
- doctest documentation: https://docs.python.org/3/library/doctest.html
- Issue 443: https://github.com/collective/icalendar/issues/443

This file should be tests, too:

    >>> print("Hello World!")
    Hello World!

"""

import doctest
import importlib
import pathlib

import pytest

HERE = pathlib.Path(__file__).parent
PROJECT_PATH = HERE.parent

PYTHON_FILES = list(PROJECT_PATH.rglob("*.py"))
DOCS_PATH = PROJECT_PATH.parent / "docs"
RST_FILES = list(DOCS_PATH.rglob("*.rst")) + [PROJECT_PATH.parent / "README.rst"]

MODULE_NAMES = [
    "icalendar_compatibility",
]


@pytest.mark.parametrize("module_name", MODULE_NAMES)
def test_docstring_of_python_file(module_name):
    """This test runs doctest on the Python module."""
    module = importlib.import_module(module_name)
    test_result = doctest.testmod(module, name=module_name)
    assert test_result.failed == 0, f"{test_result.failed} errors in {module_name}"


# This collection needs to exclude .tox and other subdirectories
DOCUMENT_PATHS = RST_FILES + PYTHON_FILES


def test_this_file_is_also_tested():
    """Check we recurse."""
    paths = list(map(str, DOCUMENT_PATHS))
    print("Documents:\n", "\n".join(paths))
    assert __file__ in paths


def doctest_print(obj):
    """doctest print"""
    if isinstance(obj, bytes):
        obj = obj.decode("UTF-8")
    print(str(obj).strip().replace("\r\n", "\n").replace("\r", "\n"))


@pytest.mark.parametrize("document", DOCUMENT_PATHS)
def test_documentation_file(document):
    """This test runs doctest on a documentation file.

    functions are also replaced to work.
    """
    test_result = doctest.testfile(
        str(document),
        module_relative=False,
        globs={"print": doctest_print},
        raise_on_error=False,
    )
    assert test_result.failed == 0, f"{test_result.failed} errors in {document.name}"
