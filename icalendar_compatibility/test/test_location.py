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
from urllib.parse import quote, unquote

import pytest
from icalendar import Event, vGeo

from icalendar_compatibility import Location, LocationSpec


def test_altrep(location_altrep: Location):
    """Check the usage of altrep."""
    assert location_altrep.url == "https://www.openstreetmap.org/relation/62422"
    assert location_altrep.text == "Berlin"


def test_geo_in_location_text(location_geo_misplaced: Location):
    """Check the link is as expected."""
    assert location_geo_misplaced.text == "50.1075325012207, 14.2693090438843"


def test_geo_in_location_geo(
    location_geo_misplaced: Location, location_spec: LocationSpec
):
    """Check the link is as expected."""
    assert location_geo_misplaced.lat == 50.1075325012207
    assert location_geo_misplaced.lon == 14.2693090438843
    assert location_geo_misplaced.zoom == location_spec.zoom


def test_geo_location_given(location_geo: Location, location_spec: LocationSpec):
    """Check that we have the namme and a URL."""
    assert location_geo.lat == 37.386013
    assert location_geo.lon == -122.082932
    assert location_geo.geo == vGeo((37.386013, -122.082932))
    assert location_geo.zoom == location_spec.zoom


def test_we_generate_the_link_from_the_location_text(
    location_text: Location, location_spec: LocationSpec
):
    """We generate a link."""
    assert location_text.text == "Berlin"
    assert location_text.url == location_spec.get_text_url(
        location="Berlin", zoom=location_spec.zoom
    )


def test_link_from_geo_1(location_geo: Location, location_spec: LocationSpec):
    assert (
        location_geo.text
        == "Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika"
    )
    assert location_geo.url == location_spec.get_geo_url(
        lat=37.386013, lon=-122.082932, zoom=location_spec.zoom
    )


def test_link_from_geo_2(location_geo_misplaced: Location, location_spec: LocationSpec):
    assert location_geo_misplaced.url == location_spec.get_geo_url(
        lat=50.1075325012207, lon=14.2693090438843
    )


def test_get_geo_url():
    assert (
        LocationSpec(geo_url="{lat}x{lon}", text_url="").get_geo_url(lat=50, lon=14)
        == "50x14"
    )
    assert (
        LocationSpec(geo_url="{lat}x{lon}, z={zoom}", text_url="").get_geo_url(
            lat=50, lon=14
        )
        == "50x14, z=16"
    )
    assert (
        LocationSpec(geo_url="{lat}x{lon}, z={zoom}", text_url="").get_geo_url(
            lat=5, lon=1, zoom=4
        )
        == "5x1, z=4"
    )


def test_Location_with_no_location(no_location: Location):
    """Check that the location is empty."""
    assert no_location.text == ""
    assert no_location.url == ""


def test_url_in_location_counts_as_url(location_link):
    """If we have a URL in the location, we use the first URL as the location URL."""
    assert location_link.url == "https://www.berlin.de/"
    assert location_link.text == " We meet in https://www.berlin.de/ "


@pytest.mark.parametrize(
    ("forbidden_content"),
    [
        "/../../../",
        "?asd=asd",
        "..",
        " asd ",
        "?a",
        "\r\n",
    ],
)
def test_location_information_is_inserted_url_escaped(forbidden_content):
    """We should test that the / is escaped and that characters like ? do not appear. They would break the URL.

    Escape:
    - spaces and other characters
    - dots
    - slash
    - ?
    """
    event = Event()
    event.add("LOCATION", forbidden_content)
    location = Location(event)
    assert forbidden_content not in location.url
    quoted = LocationSpec.quote(forbidden_content)
    assert quoted in location.url


INVALID_EVENT_GEO = """
BEGIN:VEVENT
GEO:12/../../..,123
END:VEVENT
"""


def test_geo_location_is_also_escaped():
    """The geo location should not work with bad input."""
    event = Event.from_ical(INVALID_EVENT_GEO)
    location = Location(event)
    assert location.url == ""
    assert location.lat is None
    assert location.lon is None
    assert location.geo is None


def test_location_with_unicode():
    """Test that the location works with unicode."""
    event = Event()
    name = "České Budějovice"
    event.add("LOCATION", name)
    location = Location(event)
    assert name not in location.url
    assert quote(name) in location.url


def test_replace_spec_with_empty_spec(location_geo: Location):
    """The spec can be empty."""
    location_geo.spec = LocationSpec.for_no_url()
    assert location_geo.url == ""


def test_quote_unquote():
    """Make sure we can quote and unquote all the strings."""
    for i in range(256):
        c = chr(i)
        assert unquote(LocationSpec.quote(c)) == c


@pytest.mark.parametrize("char", ["%", "=", "?", "/", "&", ".", "<", ">", '"', "'"])
def test_quote_certain_characters(char):
    quoted = LocationSpec.quote(char)
    assert quoted.startswith("%")
    assert quoted != char
