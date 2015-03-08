This is a work in progress. I had a need for some services to automate admin tasks in RabbitMQ, so I decided to start building some things.


### Account Creator

This service creates and binds an admin only exchange/routing key (`account_creator`) and begins listening for messages. A new RabbitMQ user/password/virtual host will be created for each message. The resulting connection information is passed to a user-defined handler method. You to decide what to do with it from there.


### Account Destroyer

This service creates and binds an admin only exchange/routing key (`account_destroyer`) and begins listening for messages. Each message contains a single property (`user`) that is a user name you want deleted.


### Connection Manager

This service calls a user-defined method that supplies a map of RabbitMQ user names to integers representing the maximum number of concurrent connections allowed for each user. It checks the current number of open connections for each, if the count is above the maximum it closes connections (starting with oldest) to maintain the maximum.
