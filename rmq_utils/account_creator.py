import random
import string

from pyrabbit.api import Client


def random_string(size=6):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])


class AccountCreator(object):

    def __init__(self, admin_host, admin_user, admin_password):
        self._admin_host = admin_host
        self._admin_user = admin_user
        self._admin_password = admin_password
        self._management_api = self._connect_to_management_api()

    def _connect_to_management_api(self):
        return Client(self._admin_host, self._admin_user, self._admin_password)

    def _create_account(self):
        username = random_string(8)
        password = random_string(32)

        self._management_api.create_user(username, password)
        self._management_api.create_vhost(username)
        self._management_api.set_vhost_permissions(username, username, ".*", ".*", ".*")

        return {
            'username': username,
            'password': password,
            'vhost': username
        }
