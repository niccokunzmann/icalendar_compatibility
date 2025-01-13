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

from icalendar_compatibility import Event

HERE = Path(__file__).parent
EVENTS = HERE / "events"

for file in EVENTS.iterdir():
    if file.suffix == ".ics":
        def _fixture(path:Path=file) -> Event:
            """Create an event adapter."""
            cal = Calendar.from_ical(path.read_text())
            return Event(cal.events[0])
        pytest.fixture(name=file.stem)(_fixture)
