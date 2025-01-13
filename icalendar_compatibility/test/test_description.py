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
"""Test getting the description of calendar files."""

from icalendar_compatibility.description import Description


def test_no_description_is_there(no_description:Description):
    """We should have no description."""
    assert no_description.text == ""
    assert no_description.html == ""

def test_html_description_is_recognized(description_html:Description):
    """Check that we recognize the HTML description."""
    
