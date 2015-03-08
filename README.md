This is a work in progress. I had a need for some services to automate admin tasks in RabbitMQ, so I decided to start building some things.


### Account Creator

Subclass, then implement two user-defined methods:
* One that will get a list of accounts to create
* One that will be called upon completion of account creation


### Account Destroyer

TBD


### Connection Manager

This service calls a user-defined method that supplies a map of RabbitMQ user names to integers representing the maximum number of concurrent connections allowed for each user. It checks the current number of open connections for each, if the count is above the maximum it closes connections (starting with oldest) to maintain the maximum.
