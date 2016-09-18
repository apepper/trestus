trestus
=======
Trestus is a static status page generator that uses a `Trello <https://trello.com/>`_ board as a data source.

It was inspired by the excellent `statuspage <https://github.com/jayfk/statuspage>`_ project, which uses Github issues to drive a status page, and then stores on the same repo to be served via Github Pages, and `The Changelog Weekly <https://changelog.com/weekly/>`_, who use `Trello as a CMS <https://changelog.com/trello-as-a-cms/>`_ to generate their insanely useful newsletter.

Why?
----

Because you should be informing your customers of outages and issues affecting the services they use, and Trello is a very fast and easy to use interface for defining outages and investigations through kanban cards/lanes.

How does it work?
-----------------

Trestus expects the board you tell it about to be setup on Trello with some specific lanes and labels available.

When you add a card to the **Reported** or **Investigating** lane, label it with a severity and at least one service name, the card will show up in any one of those states on the generated status page.


Trello:

.. image:: images/trello1.png

Trestus output:

.. image:: images/status1.png
    :scale: 50%


Your card can include markdown like any other Trello card and that will be converted to HTML on the generated status page, and any comments to the card will show up as updates to the status (and yes, markdown works in these too).


Trello:

.. image:: images/trello2.png

Trestus output:

.. image:: images/status2.png
    :scale: 50%


When the outage has been solved, moving the card to the **Fixed** lane will resolve it (putting the status back into the green but keeping any descriptions/comments as historical backlog underneath).


Trello:

.. image:: images/trello3.png

Trestus output:

.. image:: images/status3.png
    :scale: 50%

Lanes
*****

 * **Reported**
 * **Investigating**
 * **Fixed**

Labels
******

 * **status:degraded performance**
 * **status:major outage**

Any other label you add (without the 'status:' prefix) will be a service name.

Installation
------------

From PyPI with pip:

.. code-block::
    
    $ venv ./trestus-env
    $ ./trestus-env/bin/pip install trestus


As a `snap package <https://snapcraft.io/>`_:

.. code-block::
    
    $ sudo snap install trestus

Usage
-----

.. code-block::
            
    usage: trestus [-h] [-k KEY] [-s SECRET] [-t TOKEN] [-S TOKEN_SECRET] [-b BOARD] [-T TEMPLATE] [-d TEMPLATE_DATA] output_path
    
    Generate a status page from a Trello board
    
    positional arguments:
      output_path           Path to output rendered HTML to
    
    optional arguments:
      -h, --help            show this help message and exit
      -k KEY, --key KEY     Trello API key
      -s SECRET, --secret SECRET
                            Trello API secret
      -t TOKEN, --token TOKEN
                            Trello API auth token
      -S TOKEN_SECRET, --token-secret TOKEN_SECRET
                            Trello API auth token secret
      -b BOARD, --board-id BOARD
                            Trello board ID
      -T TEMPLATE, --custom-template TEMPLATE
                            Custom jinja2 template to use instead of default
      -d TEMPLATE_DATA, --template-data TEMPLATE_DATA
                            If using --custom-template, you can provide a YAML file to load in data that would be available in the template the template
      --skip-css            Skip copying the default trestus.css to the output dir.


Example usage
*************

.. code-block::
    
    trestus -k <trello key> -s <trello secret> -t <trello auth token> -S <trello auth token secret> -b <board ID> ./test.html

This will generatea ``test.html`` in your current directory, and also copy over ``trestus.css`` (to skip this and use your own CSS, use the ``--skip-css`` option).


How do I hook it up to Trello?
------------------------------


