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

import pytest

from icalendar_compatibility.description import Description


def test_no_description_is_there(no_description: Description):
    """We should have no description."""
    assert no_description.text == ""
    assert no_description.html == ""


def test_html_description_is_recognized(description_html: Description):
    """Check that we recognize the HTML description."""
    assert (
        description_html.html
        == 'Marceline Car Show - <a href="https://www.MarcelineCarShow.com">https://www.MarcelineCarShow.com</a>'
    )
    assert description_html.text == ""


@pytest.mark.parametrize(
    ("s", "is_html"),
    [
        ("<", False),
        (">", False),
        ("<a>", True),
        (
            'Marceline Car Show - <a href="https://www.MarcelineCarShow.com">https://www.MarcelineCarShow.com</a>',
            True,
        ),
        (
            "jhaskjfhajkfh jahskjd haskhk asdkjahs, asjdhajsjf../asdaskjfk < nannana  kajskldhlkas\naskjdlkasjld > akshdj",
            False,
        ),
    ],
)
def test_html_probability(s, is_html):
    """Test the HTML recognition."""
    assert Description.this_could_be_html(s) == is_html


def test_altrep(description_altrep_html: Description):
    """Check that we can have both: text and html."""
    assert (
        description_altrep_html.text
        == "Know This Heading!\n\nPlease have a look at this website:\nExamples\n🙂\n\n    one\n    two\n\nAnd consider this:\n\n    a bullet point\n    and another bullet point\n\nbold, underlined and italic work!\n\ncode\ncode\ncode"
    )
    assert (
        description_altrep_html.html
        == '<h1>Know This Heading!</h1><br>Please have a look at this website:<br><a href="https://open-web-calendar.quelltext.eu/templates/">Examples</a><br>🙂<ol><li>one</li><li>two</li></ol>And consider this:<ul><li>a bullet point</li><li>and another bullet point</li></ul><p><b>bold</b>, <u>underlined</u> and <i>italic</i> work!</p><pre>code<br>code<br>code</pre>'
    )


def test_recognize_x_alt_desc(x_alt_description: Description):
    """Recognize the alternative description."""
    assert (
        x_alt_description.html
        == "<p>Estudio</p><p><em>Presentan: Tomás Lambertini </em>y <em>Pablo Porcel</em></p><p><em>Habrá café y alimentos biodinámicos. Aporte económico voluntario.</em></p>"
    )
    assert (
        x_alt_description.text
        == "Estudio\n\nPresentan: Tomás Lambertini y Pablo Porcel\n\nHabrá café y alimentos biodinámicos. Aporte económico voluntario."
    )
