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
"""Event description computation."""

from icalendar import Event


class Description:
    """Event description compatibility."""

    def __init__(self, event: Event):
        """Create a new Description extraction for the event."""
        self._event = event

    @property
    def html(self) -> str:
        r"""The event description as HTML.

        The HTML description is stored in different places.
        This extracts the HTML description.

        Example:

        .. code-block:: python

            >>> from icalendar import Event
            >>> from icalendar_compatibility import Description
            >>> event = '''
            ... BEGIN:VEVENT
            ... SUMMARY:Eventwith HTML
            ... DTSTART;TZID=Europe/London:20240414T090000
            ... DESCRIPTION;ALTREP="data:text/html,%3Ch1%3EKnow%20This%20Heading!%3C%2Fh1%3
            ... E%3Cbr%3EPlease%20have%20a%20look%20at%20this%20website%3A%3Cbr%3E%3Ca%20hr
            ... ef%3D%22https%3A%2F%2Fopen-web-calendar.quelltext.eu%2Ftemplates%2F%22%3EEx
            ... amples%3C%2Fa%3E%3Cbr%3E%F0%9F%99%82%3Col%3E%3Cli%3Eone%3C%2Fli%3E%3Cli%3Et
            ... wo%3C%2Fli%3E%3C%2Fol%3EAnd%20consider%20this%3A%3Cul%3E%3Cli%3Ea%20bullet%
            ... 20point%3C%2Fli%3E%3Cli%3Eand%20another%20bullet%20point%3C%2Fli%3E%3C%2Ful
            ... %3E%3Cp%3E%3Cb%3Ebold%3C%2Fb%3E%2C%20%3Cu%3Eunderlined%3C%2Fu%3E%20and%20%3
            ... Ci%3Eitalic%3C%2Fi%3E%20work!%3C%2Fp%3E%3Cpre%3Ecode%3Cbr%3Ecode%3Cbr%3Ecod
            ... e%3C%2Fpre%3E":Know This Heading!\n\nPlease have a look at this website:\nE
            ... xamples\n🙂\n\n    one\n    two\n\nAnd consider this:\n\n    a bullet poi
            ... nt\n    and another bullet point\n\nbold\, underlined and italic work!\n\nc
            ... ode\ncode\ncode
            ... END:VEVENT
            ... '''
            

            
        """

__all__ = ["Description"]
