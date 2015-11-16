# Bugyou

An Automatic Bug Reporting Tool

# How it works?

The `Bugyou Consumer` listens to fedmsg for all the messages. Once message
arrives it queues it in the retask queues.
The plugins of bugyou consumes from the retask queues and filters the message
based on the topic they are subscribed to.
Once the plugin gets the designated message it processes it and files a bug
into the bug tracking tools like (trac, pagure) etc.

The list of plugins would be maitained in bugyou_plugins.conf in the given
format

``
[autocloud]
topic = org.fedoraproject.prod.autocloud.image.failed,
org.fedoraproject.prod.autocloud.image.success
klass = bugyou_plugins.autocloud.plugin:AutocloudPlugin
``

The plugin can be started using the command `bugyouctl start autocloud`. This
is start the plugin and send a request to bugyou daemon to create designated
queue for the plugin. Once the queue is ready `Bugyou Consumer` will start
pushing messages to that plugin and the new plugin will start consuming those
messages
