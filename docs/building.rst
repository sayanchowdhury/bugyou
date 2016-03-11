Development
===========

Bugyou is written in Python2.

Clone the repo from pagure.
::

    $ git clone ssh://git@pagure.io/bugyou.git
    $ git clone ssh://git@pagure.io/bugyou_plugins.git

Create a virtualenv, here we will be using virtualenvwrapper
::

    $ mkvirtualenv bugyou

Activate the virtualenv
::
    $ workon bugyou

Run ``python setup.py develop`` in both the directories ``bugyou`` and
``bugyou_plugins``.

Make sure that redis in running.

In the ``bugyou`` repo, run ``fedmsg-hub`` start the daemon.
::
    $ fedmsg-hub

In the ``bugyou_plugins`` repo, run ``bugyou-cntrl`` which will start the
controller.

Configuration
=============

``bugyou`` has two configuration files

* bugyou_plugins.cfg
* bugyou_services.cfg




