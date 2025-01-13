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

from pathlib import Path

import pytest
from icalendar import Calendar

from icalendar_compatibility import Location, LocationSpec

HERE = Path(__file__).parent
EVENTS = HERE / "events"

for file in EVENTS.iterdir():
    if file.suffix.lower() == ".ics" and "location" in file.stem:

        def _fixture(location_spec: LocationSpec, path: Path = file) -> Location:
            """Create an event adapter."""
            cal = Calendar.from_ical(path.read_text())
            assert (
                len(cal.events) == 1
            ), f"We need one event only, not {len(cal.events)} in {path.stem}"
            return Location(cal.events[0], location_spec)

        locals()[file.stem] = pytest.fixture(_fixture)


@pytest.fixture(
    params=[
        LocationSpec.for_openstreetmap_org,
        LocationSpec.for_bing_com,
        LocationSpec.for_google_co_uk,
    ]
)
def location_spec(request) -> LocationSpec:
    """The default spec."""
    return request.param()
