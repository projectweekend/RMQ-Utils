This is a work in progress. I had a need for some services to automate admin tasks in RabbitMQ, so I decided to start building some things.


### Account Creator

A class that makes two connections to RabbitMQ:
* One on localhost for issuing API commands to create new users for the server.
* One on an external URL that will receive messages for each user to create.

Subclass, then implement a user-defined method:
* One that will be called upon completion of account creation (post-create)


### Account Destroyer

A class that makes two connections to RabbitMQ:
* One on localhost for issuing API commands to create new users for the server.
* One on an external URL that will receive messages for each user to destroy.

Subclass, then implement a user-defined method:
* One that will be called upon completion of account delete (post-delete)


### Connection Manager

This service calls a user-defined method that supplies a map of RabbitMQ user names to integers representing the maximum number of concurrent connections allowed for each user. It checks the current number of open connections for each, if the count is above the maximum it closes connections (starting with oldest) to maintain the maximum.
