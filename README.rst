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
    
    trestus -k <trello key> -s <trello secret> -t <trello auth token> \
    -S <trello auth token secret> -b <board ID> ./test.html

This will generatea ``test.html`` in your current directory, and also copy over ``trestus.css`` (to skip this and use your own CSS, use the ``--skip-css`` option).

If you want to provide your own Jinja2 template for generating the status page, you can use the ``-T``/``--custom-template`` option.

For example we use this feature to translate our Three-Letter-Acronyms for service to more customer friendly long-form names, by pairing with the ``-d``/``-template-data`` option to pass in a YAML dict of aliases:

.. code-block::
    
    trestus -k <trello key> -s <trello secret> -t <trello auth token> \
    -S <trello auth token secret> -b <board ID> --T mystatus.html.j2 \
    -d myaliases.yaml --skip-css ./test.html

As mentioned above, we're also using the ``--skip-css`` flag here to skip copying the default template CSS over, and instead use our own to apply a different logo/styling etc.


How do I hook it up to Trello?
------------------------------

The way I have achieved this is by creating a "secret" URL routed to a VM that runs a script which invokes trestus with the ``flock`` utility to limit invocations in a queue.

I then hooked this address up to a webhook on the right Trello board, using Trello's `webhook API <FILLTHISIN>`_, so now whenver a change happens on the board an invocation of trestus is queued up on the target host.

**Nota bene**: be careful about how this webhook handler is exposed, for example I have allowed only GET/POST in this situation as these are the actions Trello expect to be available (for verification, and hook postbacks respectively), but the URL also has a randomly generated portion.

Bugs, issues, improvements, features requests and support
---------------------------------------------------------

If you have discovered an issue with trestus, or have an idea for improving it, please feel free to `hit up GitHub issues <https://github.com/canonical-ols/trestus/issues>`_ and I'll work with you to improve things. :heart: :smile:
