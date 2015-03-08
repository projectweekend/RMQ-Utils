This is a work in progress. I had a need for some services to automate admin tasks in RabbitMQ, so I decided to start building some things.


### Account Creator

This service calls a user-defined method that supplies a list of tasks. A new RabbitMQ user/password/virtual host will be created for each task. The resulting connection information is passed to another user-defined handler method. You to decide what to do with it from there.


### Account Destroyer

This service calls a user-defined method that supplies a list of RabbitMQ user names. Each user in the list will be deleted.


### Connection Manager

This service calls a user-defined method that supplies a map of RabbitMQ user names to integers representing the maximum number of concurrent connections allowed for each user. It checks the current number of open connections for each, if it is above the maximum it closes connections (starting with oldest) to maintain the maximum.
