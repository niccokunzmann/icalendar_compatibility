Usage
=====

``icalendar_compatibility`` is based on `icalendar`.
The information is extracted from the icalendar components and more compatibility with other ics generators is provided.


Event Description
-----------------

It would be nice if there was a uniform way for **text** and **HTML** description in icalendar.
However, sometimes HTML and text get thrown into the same field or encoded in different places.
:class:`icalendar_compatibility.Description` takes care of this.

In this example, we consider an event from the Gancio Calendar:

.. code-block:: python

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

.. code-block:: python

    >>> from icalendar_compatibility import Description
    >>> description = Description(event)
    >>> description.text[:26]
    'Estudio\n\nPresentan: Tomás'
    >>> description.html[:38]
    '<p>Estudio</p><p><em>Presentan: Tomás'

The example above is just one of many in which the HTML description is in an unexpected place.

Compatibility for Description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We tested :class:`icalendar_compatibility.Description` to be compatibile with :rfc:`5545`, `Mozilla Thunderbird`, `Gancio`, `CMS4Schools.com`.

Event Location
--------------

Location information can be located in the ``LOCATION`` and the ``GEO`` field of :rfc:`5545` events.
This module creates a unified interface using :class:`icalendar_compatibility.Location`.

In order to extract location information from an event, we have to generate an event first.
The event in this example has a ``GEO`` location and an ``LOCATION`` description.

.. code-block:: python

    >>> from icalendar import Event
    >>> event_in_mountain_view = '''
    ... BEGIN:VEVENT
    ... SUMMARY:Event in Mountain View with Geo link
    ... DTSTART:20250115T150000Z
    ... LOCATION:Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika
    ... GEO:37.386013;-122.082932
    ... END:VEVENT
    ... '''
    >>> event = Event.from_ical(event_in_mountain_view)



The specification :class:`icalendar_compatibility.LocationSpec` changes how we extract event information.
In this example, we use Bing Maps.

.. code-block:: python

    >>> from icalendar_compatibility import LocationSpec
    >>> spec = LocationSpec.for_bing_com()
    >>> spec.zoom
    16

The :class:`icalendar_compatibility.Location` has insight into different attributes of the event.


.. code-block:: python

    >>> from icalendar_compatibility import Location
    >>> location = Location(event, spec)
    >>> print(location.text)  # using LOCATION
    Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika
    >>> print(location.url)   # using GEO
    https://www.bing.com/maps?brdr=1&cp=37.386013%7E-122.082932&lvl=16

Compatibility for Location
~~~~~~~~~~~~~~~~~~~~~~~~~~

We tested :class:`icalendar_compatibility.Location` to be compatibile with :rfc:`5545`, `Mozilla Thunderbird`, `regiojet.cz`.

Preconfigured Maps
------------------

We have several maps already preconfigured:

- https://openstreetmap.org - :func:`icalendar_compatibility.LocationSpec.for_openstreetmap_org`
- https://www.bing.com/maps - :func:`icalendar_compatibility.LocationSpec.for_bing_com`
- https://www.google.com/maps - :func:`icalendar_compatibility.LocationSpec.for_google_com`
- https://www.google.co.uk/maps - :func:`icalendar_compatibility.LocationSpec.for_google_co_uk`
- no map - :func:`icalendar_compatibility.LocationSpec.for_no_url`

Custom Maps
-----------

You can configure your own url templates.
This is useful when:

- You host your own map.
- You want to use a custom search.
- You want to adapt a map that exists to add your language.

This section should help you out.

There are two types of URLs to generate.

.. _custom-map-spec:

- A URL can be based on the **text** of the **LOCATION**.
  
    This can be a text like ``Berlin``.
    Urls of this type usually search for the location to display.

    Parameters:

    - ``{location}`` - this is **required**
    
        This will be replaced with the text in the **LOCATION** field of the event.

    - ``{zoom}`` - this is **optional**
    
        The map can have a zoom parameter to open it at a certain zoom level. 

    Example:

    .. code-block::

        https://www.google.com/maps/search/{location}

- A URL can be based on the **GEO** information of the event providing **longitude** and **latitude**.

    These urls do not know the name of the location but can open precisely there.

    Parameters:

    - ``{lon}`` - this is **required**
  
        This is replaced with the longitude of the event.
    
    - ``{lat}`` - this is **required**
  
        This is replaced with the latitude of the event.

    - ``{zoom}`` - this is **optional**
  
        The map can have a zoom parameter to open it at a certain zoom level. 

    Example:

    .. code-block::

        https://www.google.com/maps/@{lat},{lon},{zoom}z


The example below create a specification for a custom map:

.. code-block:: python

    >>> from icalendar_compatibility import LocationSpec
    >>> my_map_spec = LocationSpec(
    ...     text_url="https://my.map/search?q={location}",  # you could add the optional {zoom} parameter
    ...     geo_url="https://my.map/#{lat}/{lon}"           # you can add the optional {zoom} parameter
    ... )

With the cusom map configured, the URL for an event in Berlin can be seen below:

.. code-block:: python

    >>> from icalendar import Event
    >>> from icalendar_compatibility import Location
    >>> event_in_berlin = """
    ... BEGIN:VEVENT
    ... LOCATION:Berlin?
    ... END:VEVENT
    ... """
    >>> location = Location(Event.from_ical(event_in_berlin), my_map_spec)
    >>> location.url
    'https://my.map/search?q=Berlin%3F'

