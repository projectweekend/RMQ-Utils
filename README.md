This is a work in progress. I had a need for some services to automate admin tasks in RabbitMQ, so I decided to start building some things.


### Account Creator

This is a class that makes one connection to the Rabbit Admin API and one to a direct exchange/queue named: `rmq_utils/account_creator`. It listens for messages, creates a new Rabbit user/password/vhost and then calls a `post_create` method for each. The message must be formatted JSON like so:

```json
{
    "user_key": "whatever"
}
```

The `post_create` method must be implemented in a sub-class. It will receive two input parameters:

* `user_key` - The same value received in the message
* `credentials` - A dictionary representing the Rabbit account info for the account that was just created. It has the following keys: `username`, `password`, `vhost`

**Example:**
```python
from rmq_utils import AccountCreator

class ExampleAccountCreator(AccountCreator):

    @staticmethod
    def post_create(user_key, creds):
        # Do whatever you want here, perhaps make a call to
        # update a record in a database using the user_key
        print('{0}: {1}'.format(user_key, creds['username']))


def main():
    creator = ExampleAccountCreator(
        rabbit_url='rabbit-url-to-listen-for-messages',
        mgmt_host='rabbit-host-to-perform-admin-actions',
        mgmt_user='admin-user',
        mgmt_password='admin-password')
    try:
        creator.run()
    except KeyboardInterrupt:
        creator.stop()


if __name__ == '__main__':
    main()
```


### Account Destroyer

A class that makes two connections to RabbitMQ:
* One on localhost for issuing API commands to create new users for the server.
* One on an external URL that will receive messages for each user to destroy.

Subclass, then implement a user-defined method:
* One that will be called upon completion of account delete (post-delete)


### Connection Manager

This service calls a user-defined method that supplies a map of RabbitMQ user names to integers representing the maximum number of concurrent connections allowed for each user. It checks the current number of open connections for each, if the count is above the maximum it closes connections (starting with oldest) to maintain the maximum.
