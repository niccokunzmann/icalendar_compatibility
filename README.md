# Compatibility for ICalendar

ICS files, altough specified by [RFC 5545] differ in how to specify event information.
This packages provides a unified interface.

This package is based on [icalendar].

[RFC 5545]: https://www.rfc-editor.org/rfc/rfc5545.html
[icalendar]: https://pypi.org/project/icalendar/

## Installation

```sh
pip install icalendar-compatibility
```

## Location Information

Location information can be located in the LOCATION and the GEO field of RFC5545 events.
This module creates a unified interface.

```python
>>> from icalendar_compatibility import Location, LocationSpec
>>> from icalendar import Event
>>> event_string = '''
... BEGIN:VEVENT
... SUMMARY:Event in Mountain View with Geo link
... DTSTART:20250115T150000Z
... LOCATION:Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika
... GEO:37.386013;-122.082932
... END:VEVENT
... '''
>>> event = Event.from_ical(event_string)
>>> location = Location(event, LocationSpec.bing_com())
>>> print(location.text)
Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika
>>> print(location.url)
https://www.bing.com/maps?brdr=1&cp=37.386013%7E-122.082932&lvl=16

```
