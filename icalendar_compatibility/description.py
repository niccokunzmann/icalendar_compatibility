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

import re
from urllib.parse import unquote

from icalendar import Event, vText

RE_HTML_TAGS_PROPER = re.compile(r"^([^<]*(<\S[^<>]*>))+[^<]*$")


class Description:
    r"""Event description compatibility.

    This includes HTML and text description.

    Example:

    .. code-block:: python

        >>> from icalendar import Event
        >>> from icalendar_compatibility import Description
        >>> event_string = '''
        ... BEGIN:VEVENT
        ... SUMMARY:Eventwith HTML
        ... DTSTART;TZID=Europe/London:20240414T090000
        ... DESCRIPTION;ALTREP="data:text/html,%3Ch1%3EKnow%20This%20Heading!%3C%2Fh1%3
        ...  E%3Cbr%3EPlease%20have%20a%20look%20at%20this%20website%3A%3Cbr%3E%3Ca%20hr
        ...  ef%3D%22https%3A%2F%2Fopen-web-calendar.quelltext.eu%2Ftemplates%2F%22%3EEx
        ...  amples%3C%2Fa%3E%3Cbr%3E%F0%9F%99%82%3Col%3E%3Cli%3Eone%3C%2Fli%3E%3Cli%3Et
        ...  wo%3C%2Fli%3E%3C%2Fol%3EAnd%20consider%20this%3A%3Cul%3E%3Cli%3Ea%20bullet%
        ...  20point%3C%2Fli%3E%3Cli%3Eand%20another%20bullet%20point%3C%2Fli%3E%3C%2Ful
        ...  %3E%3Cp%3E%3Cb%3Ebold%3C%2Fb%3E%2C%20%3Cu%3Eunderlined%3C%2Fu%3E%20and%20%3
        ...  Ci%3Eitalic%3C%2Fi%3E%20work!%3C%2Fp%3E%3Cpre%3Ecode%3Cbr%3Ecode%3Cbr%3Ecod
        ...  e%3C%2Fpre%3E":Know This Heading!\\n\\nPlease have a look at this website:\\nE
        ...  xamples\\n🙂\\n\\n    one\\n    two\\n\\nAnd consider this:\\n\\n    a bullet poi
        ...  nt\\n    and another bullet point\\n\\nbold\\, underlined and italic work!\\n\\nc
        ...  ode\\ncode\\ncode
        ... END:VEVENT
        ... '''
        >>> event = Event.from_ical(event_string)
        >>> description = Description(event)
        >>> description.html[:49]
        '<h1>Know This Heading!</h1><br>Please have a look'
        >>> description.text[:38]
        'Know This Heading!\n\nPlease have a look'

    .. note::

        Please note that sometimes there is an HTML description but not a text
        description.

    .. code-block:: python

        >>> event_string = '''
        ... BEGIN:VEVENT
        ... SUMMARY:Eventwith HTML
        ... DTSTART;TZID=Europe/London:20240414T090000
        ... DESCRIPTION:<p>HTML description</p>
        ... END:VEVENT
        ... '''
        >>> event = Event.from_ical(event_string)
        >>> description = Description(event)
        >>> description.html
        '<p>HTML description</p>'
        >>> description.text
        ''

    """

    def __init__(self, event: Event):
        """Create a new Description extraction for the event."""
        self._event = event

    @property
    def raw_description(self) -> vText:
        """The raw desctiption from the event.."""
        return self._event.get("DESCRIPTION", vText(""))

    @property
    def html(self) -> str:
        r"""The event description as HTML.

        The HTML description is stored in different places.
        This extracts the HTML description.

        """
        description = self.raw_description
        # print(self._event)
        altrep = description.params.get("ALTREP")
        # print("altrep", description, description.params)
        if altrep is not None and "," in altrep:
            data, content = altrep.split(",", 1)
            if data == "data:text/html":
                # Thunderbird html
                return unquote(content)
        # CMS4Schools.com
        altdesc = self._event.get("X-ALT-DESC")
        if (
            altdesc is not None
            and hasattr(altdesc, "params")
            and altdesc.params.get("FMTTYPE") == "text/html"
        ):
            return str(altdesc)
        if self.this_could_be_html(description):
            return str(description)
        return ""

    @property
    def text(self) -> str:
        """The text description of the event or an empty string."""
        description = str(self.raw_description)
        if description == self.html:
            return ""
        return str(description)

    @staticmethod
    def this_could_be_html(description: str):
        """Wether this is possibly HTML."""
        return bool(RE_HTML_TAGS_PROPER.match(description))


__all__ = ["Description"]
