Usage
=====

``icalendar_compatibility`` is based on `icalendar`.
The information is extracted from the icalendar components and more compatibility with other ics generators is provided.

In order to extract information, we have to generate an event first.

.. code:: python

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


Location Information
--------------------

Location information can be located in the ``LOCATION`` and the ``GEO`` field of :rfc:`5545` events.
This module creates a unified interface using :class:`icalendar_compatibility.Location`.

The specification :class:`icalendar_compatibility.LocationSpec` changes how we extract event information.
In this example, we use Bing Maps.

.. code:: python

    >>> from icalendar_compatibility import LocationSpec
    >>> spec = LocationSpec.for_bing_com()
    >>> spec.zoom
    16

The :class:`icalendar_compatibility.Location` has insight into different attributes of the event.


.. code:: python

    >>> from icalendar_compatibility import Location
    >>> location = Location(event, spec)
    >>> print(location.text)
    Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika
    >>> print(location.url)
    https://www.bing.com/maps?brdr=1&cp=37.386013%7E-122.082932&lvl=16


