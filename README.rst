smartversion 
============

Parse and manipulate version numbers, painlessly.

smartversion can parse and manipulate software version numbers. It's semver-compatible, and can handle a vast variety of version formats (based on real-world data).

Demo:

.. code-block:: pycon

    >>> from smartversion import Version 
    >>> v = Version.parse('linux-2.4.6-rc1') 
    >>> v.name
    linux
    >>> v.major
    2
    >>> v.minor
    4
    >>> v.patch
    '6-rc1'
    >>> v.patch1
    6
    >>> v.patch_str
    '-rc'
    >>> v.patch2
    1
    >>> v2 = Version.parse('linux-2.4.6-rc4')
    >>> v < v2
    True
    >>> v3 = Version.parse('linux-2.4.6')
    >>> v2 < v3
    True    # yes, the release candidate comes first :o)

    # You can also set version parameters explicitly
    >>> from datetime import date
    >>> v4 = Version("Bob's Amazing Software", 1, 0)
    >>> str(v4)
    Bob's Amazing Software 1.0

    # And compare versions based on age
    >>> v5 = Version("Bob's Amazing Software", 1, 2, \
               release_date=date(2009, 5, 1))
    >>> v5.is_older_than(date(2010, 1, 1)) 
    True
    >>> v4.release_date = date(2009, 1, 1)
    >>> v5.is_newer_than(v4)
    True
    >>> v5.is_older_than('2 years')
    True    # assuming you're not living in the past :o)
    ...

smarversion is like LooseVersion from distutils and parse_version from setuptools, but smarter. It was written to handle various real-world version strings that LooseVersion cannot. smartversion also does age-based comparisons based on a release date and comes with an extremely long-winded test suite. 

Features
--------

- Parses a massive range of version formats 
- Zero non-stdlib dependencies (except nose for tests)
- Version objects compare properly (==, !=, <, ...)
- Extensive test suite 
- Software age comparison 
- Human-friendly age comparison ('2 years, 3 months' / '2y3m')
- Semver-compatible (http://semver.org)

Installation
------------

To install smartversion:

.. code-block:: bash

    $ pip install smartversion

Documentation
-------------

Coming soon (:S)

