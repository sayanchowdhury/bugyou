Development
===========

Bugyou is written in Python2.

Clone the repo from pagure.
::

    $ git clone ssh://git@pagure.io/bugyou.git

Create a virtualenv, here we will be using virtualenvwrapper
::

    $ mkvirtualenv bugyou

Activate the virtualenv
::
    $ workon bugyou -no-site-packages

Install the dependencies(python-libpagure, fedmsg and fedmsg-hub) and run
fedmsg-hub
::
    $ fedmsg-hub

