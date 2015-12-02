Design
======

Bugyou is an automatic bug reporting tool. It's part of Fedora Project where it
listens to autocloud messages from fedmsg and files bug for images which have
failed the tests. Bugyou keeps updating the status of the images in the bug and
closes the issue once the tests are successful.

.. image:: diagrams/topology.png
