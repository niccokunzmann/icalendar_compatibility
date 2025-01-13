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

## Usage

```python
from icalendar_compatibility import Event

event = Event.from_icalendar()