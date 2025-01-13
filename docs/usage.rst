Usage
=====

``icalendar_compatibility`` is based on `icalendar`.
The information is extracted from the icalendar components and more compatibility with other ics generators is provided.


Description
-----------

It would be nice if there was a uniform way for text and HTML description in icalendar.
However, sometimes HTML and text get thrown into the same field or encoded in different places.
:class:`icalendar_compatibility.Description` takes care of this.

In this example, we consider an event from the Gancio Calendar:

.. code:: python

    >>> from icalendar import Event
    >>> event_string = '''
    ... BEGIN:VEVENT
    ... DESCRIPTION:Estudio\\n\\nPresentan: Tomás Lambertini y Pablo Porcel\\n\\nHabra
    ...     ́ café y alimentos biodinámicos. Aporte económico voluntario.
    ... X-ALT-DESC;FMTTYPE=text/html:<p>Estudio</p><p><em>Presentan: Tomás Lambert
    ...     ini </em>y <em>Pablo Porcel</em></p><p><em>Habrá café y alimentos biodin
    ...     ámicos. Aporte económico voluntario.</em></p>
    ... END:VEVENT
    ... '''
    >>> event = Event.from_ical(event_string)

The event has a description as HTML and as text.
We can get these descriptions easily and also with compatibility to other software.

.. code:: python

    >>> from icalendar_compatibility import Description
    >>> description = Description(event)
    >>> description.text[:26]
    'Estudio\n\nPresentan: Tomás'
    >>> description.html[:38]
    '<p>Estudio</p><p><em>Presentan: Tomás'

The example above is just one of many in which the HTML description is in an unexpected place.

Compatibility
~~~~~~~~~~~~~

We tested compatibility with :rfc:`5545`, `Mozilla Thunderbird`, `Gancio`, `CMS4Schools.com`.

Location Information
--------------------

Location information can be located in the ``LOCATION`` and the ``GEO`` field of :rfc:`5545` events.
This module creates a unified interface using :class:`icalendar_compatibility.Location`.

In order to extract location information from an event, we have to generate an event first.
The event in this example has a ``GEO`` location and an ``LOCATION`` description.

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
    >>> print(location.text)  # using LOCATION
    Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika
    >>> print(location.url)   # using GEO
    https://www.bing.com/maps?brdr=1&cp=37.386013%7E-122.082932&lvl=16

Compatibility
~~~~~~~~~~~~~

We tested compatibility with :rfc:`5545`, `Mozilla Thunderbird`, `regiojet.cz`.