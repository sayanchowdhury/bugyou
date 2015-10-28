import socket
hostname = socket.gethostname().split('.')[0]


config = {
    # Consumer stuff
    #"autocloud.consumer.enabled": True,
    #"autocloud.sqlalchemy.uri": "sqlite:////var/tmp/autocloud-dev-db.sqlite",
    "bugfiler.consumer.enabled":True,
    # Turn on logging for bugfiler
    "logging": dict(
        loggers=dict(
            bugfiler={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
}
