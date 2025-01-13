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
"""Create compatibility access for icalendar components."""

from .description import Description
from .location import Location, LocationSpec
from .version import __version__, __version_tuple__, version, version_tuple

__all__ = [
    "Description",
    "Location",
    "LocationSpec",
    "__version__",
    "__version_tuple__",
    "version",
    "version_tuple",
]
