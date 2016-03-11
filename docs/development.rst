===========
Development
===========

Bugyou is written in Python2.

- Install virtualenvwrapper::

    dnf install python-virtualenvwrapper

- Clone the ``bugyou`` repo from pagure::

    git clone ssh://git@pagure.io/bugyou.git

- Clone the ``bugyou_plugins`` repo from pagure::

    git clone ssh://git@pagure.io/bugyou_plugins.git

- Create a virtualenv, here we will be using virtualenvwrapper::

    mkvirtualenv bugyou

- Install the components in development mode::

    for i in bugyou bugyou_plugins; do pushd $i; python setup.py develop; popd; done

- Start the fedmsg daemon::

    fedmsg-hub

- Start the bugyou controller::

    bugyou-cntrl
