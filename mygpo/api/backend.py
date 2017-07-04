#
# This file is part of my.gpodder.org.
#
# my.gpodder.org is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# my.gpodder.org is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with my.gpodder.org. If not, see <http://www.gnu.org/licenses/>.
#

import uuid

from django.db import transaction, IntegrityError

from mygpo.users.settings import STORE_UA
from mygpo.users.models import Client

import logging
logger = logging.getLogger(__name__)


def get_device(user, uid, user_agent, undelete=True):
    """
    Loads or creates the device indicated by user, uid.

    If the device has been deleted and undelete=True, it is undeleted.
    """

    store_ua = user.profile.settings.get_wksetting(STORE_UA)

    # list of fields to update -- empty list = no update
    update_fields = []

    with transaction.atomic():
        try:
            client = Client(id=uuid.uuid1(), user=user, uid=uid)
            client.full_clean()
            client.save()

        except IntegrityError:
            client = Client.objects.get(user=user, uid=uid)

    if client.deleted and undelete:
        client.deleted = False
        update_fields.append('deleted')

    if store_ua and user_agent and client.user_agent != user_agent:
        client.user_agent = user_agent
        update_fields.append('user_agent')

    if update_fields:
        client.save(update_fields=update_fields)

    return client
