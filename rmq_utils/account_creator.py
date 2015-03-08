import random
import string
import json

from mixins import ManagementAPI, AsyncConsumer
from exceptions import InvalidMessageBody


def random_string(size=6):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])


class AccountCreator(ManagementAPI, AsyncConsumer):

    def __init__(self, rabbit_url, routing_key):
        self.EXCHANGE = 'rmq_utils'
        self.EXCHANGE_TYPE = 'direct'
        self.QUEUE = 'account_creator'
        self.ROUTING_KEY = routing_key
        super(AccountCreator, self).__init__(rabbit_url=rabbit_url)
        # self._management_api = self._connect_to_management_api()

    def _create_account(self, user_key):
        username = random_string(8)
        password = random_string(32)

        self._management_api.create_user(username, password)
        self._management_api.create_vhost(username)
        self._management_api.set_vhost_permissions(username, username, ".*", ".*", ".*")

        return {
            'user_key': user_key,
            'username': username,
            'password': password,
            'vhost': username
        }

    def _on_message(self, unused_channel, basic_deliver, properties, body):
        try:
            message = json.loads(body)
            user_key = message['user_key']
        except ValueError:
            self._acknowledge_message(basic_deliver.delivery_tag)
            raise InvalidMessageBody('Message body must be valid JSON')
        except KeyError:
            self._acknowledge_message(basic_deliver.delivery_tag)
            raise InvalidMessageBody('Message body must have a property: user_key')

        print(body)

        # self.post_create_handler(self._create_account(user_key))

        self._acknowledge_message(basic_deliver.delivery_tag)
