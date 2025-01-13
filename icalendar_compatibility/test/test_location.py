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
