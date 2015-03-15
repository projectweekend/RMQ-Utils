This is a work in progress. I had a need for some services to automate admin tasks in RabbitMQ, so I decided to start building some things.


### Account Creator

This is a class that makes one connection to the Rabbit Admin API and one to a direct exchange/queue named: `rmq_utils/account_creator`. It listens for messages, creates a new user/password/vhost via the Rabbit Admin API, and calls a `post_create` method for each. The message must be a JSON object:

```json
{
    "user_key": "whatever"
}
```

The `post_create` method is implemented in your sub-class. It will receive two input parameters:

* `user_key` - The same value received in the message
* `credentials` - A dictionary representing the Rabbit account info for the account that was just created. It has the following keys: `username`, `password`, `vhost`

**Example:**
```python
from rmq_utils import AccountCreator


RABBIT_URL = 'rabbit-url-to-listen-for-messages'
ADMIN_HOST = 'rabbit-admin-host'
ADMIN_USER = 'admin-user'
ADMIN_PASSWORD = 'admin-password'


class ExampleAccountCreator(AccountCreator):

    @staticmethod
    def post_create(user_key, creds):
        # Do whatever you want here, perhaps make a call to
        # update a record in a database using the user_key
        print('{0}: {1}'.format(user_key, creds['username']))


def main():
    creator = ExampleAccountCreator(
        rabbit_url=RABBIT_URL,
        mgmt_host=ADMIN_HOST,
        mgmt_user=ADMIN_USER,
        mgmt_password=ADMIN_PASSWORD)
    try:
        creator.run()
    except KeyboardInterrupt:
        creator.stop()


if __name__ == '__main__':
    main()
```


### Account Destroyer

This is a class that makes one connection to the Rabbit Admin API and one to a direct exchange/queue named: `rmq_utils/account_destroyer`. It listens for messages, deletes an existing user/vhost via the Rabbit Admin API, and calls a `post_delete` method for each. The message must be a JSON object:

```json
{
    "user_key": "whatever",
    "rabbit_user": "the_username"
}
```

The `post_delete` method is implemented in your sub-class. It will receive one input parameter:

* `user_key` - The same value received in the message

**Example:**
```python
from rmq_utils import AccountDestroyer


RABBIT_URL = 'rabbit-url-to-listen-for-messages'
ADMIN_HOST = 'rabbit-admin-host'
ADMIN_USER = 'admin-user'
ADMIN_PASSWORD = 'admin-password'


class ExampleAccountDestroyer(AccountDestroyer):

    @staticmethod
    def post_delete(user_key):
        # Do whatever you want here, perhaps make a call to
        # update a record in a database using the user_key
        print('{0}'.format(user_key))


def main():
    destroyer = ExampleAccountDestroyer(
        rabbit_url=RABBIT_URL,
        mgmt_host=ADMIN_HOST,
        mgmt_user=ADMIN_USER,
        mgmt_password=ADMIN_PASSWORD)
    try:
        destroyer.run()
    except KeyboardInterrupt:
        destroyer.stop()


if __name__ == '__main__':
    main()
```


### Connection Manager

This service maintains a map of usernames to an array of connection names. It calls a user-defined method that returns a map of usernames to integers representing the maximum number of concurrent connections allowed for each. It compares the current number of open connections for each to the max, if above the maximum it closes connections to maintain the maximum.
