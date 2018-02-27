import logging

from pulp.server.db.connection import get_collection


_logger = logging.getLogger('pulp_rpm.plugins.migrations.0042')


def migrate(*args, **kwargs):

    erratum_collection = get_collection('units_erratum')

    for errata in erratum_collection.find({}):
        erratum_collection.update({'_id': errata['_id']},
                                  {'$set': {'relogin_suggested': '', 'restart_suggested': ''}})
