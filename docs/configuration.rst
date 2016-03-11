Configuration
=============

Bugyou is configured through two configuration files that reside in
``/etc/bugyou`` directory.

1. bugyou_plugins.cfg
2. bugyou_services.cfg

bugyou_plugins.cfg
~~~~~~~~~~~~~~~~~~
This file contains the list of all the plugins along with their topic(s) they
subscribe to and the issue tracking tools they use.

::

    [plugin_name]
    services = <comma-seperated names of services>
    topic = <comma-seperated fedmsg topics>

A sample looks like::

    [autocloud]
    services = pagure
    topic = org.fedoraproject.prod.autocloud.image.success, org.fedoraproject.prod.autocloud.image.failed

In the sample above, the autocloud plugin listens to the fedmsg topics
``org.fedoraproject.prod.autocloud.image.success`` and
``org.fedoraproject.prod.autocloud.image.failed``. The only service that
autocloud uses is pagure


bugyou_services.cfg
~~~~~~~~~~~~~~~~~~~
This file primary contains the data required to use a particular service such
as API Key, repository name etc.

::

    [<plugin_name>_<service_name>]
    repo_name = <name of the repository>
    access_token = <access_token>

A sample looks like::

    [autocloud_pagure]
    repo_name = xyz
    access_token = ABC123DEF456GHI789JKL
