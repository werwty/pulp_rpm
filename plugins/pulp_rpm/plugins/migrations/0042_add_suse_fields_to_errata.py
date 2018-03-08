import logging

from pulp.server.db.connection import get_collection
from pulp.server.db.migrations.lib import utils


_logger = logging.getLogger('pulp_rpm.plugins.migrations.0042')


def migrate(*args, **kwargs):

    erratum_collection = get_collection('units_erratum')
    total_erratum_units = erratum_collection.count(
        {'relogin_suggested': {'$exists': False}, 'restart_suggested': {'$exists': False}})

    with utils.MigrationProgressLog('Erratum', total_erratum_units) as migration_log:
        for errata in erratum_collection.find(
                {'restart_suggested': {'$exists': False}},
                ['errata_id']).batch_size(100):
            erratum_collection.update({'_id': errata['_id']},
                                      {'$set': {'restart_suggested': ''}})
            migration_log.progress()

        for errata in erratum_collection.find(
                {'relogin_suggested': {'$exists': False}},
                ['errata_id']).batch_size(100):
            erratum_collection.update({'_id': errata['_id']},
                                      {'$set': {'relogin_suggested': ''}})
            migration_log.progress()