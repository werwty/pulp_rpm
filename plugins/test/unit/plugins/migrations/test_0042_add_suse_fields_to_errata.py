import unittest

from pulp.server.db.migrate.models import _import_all_the_way
import mock

migration = _import_all_the_way('pulp_rpm.plugins.migrations.0042_add_suse_'
                                'fields_to_errata')




class TestMigrate(unittest.TestCase):
    """
    Test the migrate() function.
    """
    def setUp(self):
        super(TestMigrate, self).setUp()
        self.fake_errata = {
            '_id': 'abc123'
        }

    @mock.patch.object(migration, 'get_collection')
    def test_calls_correct_functions(self, mock_get_collection):
        mock_get_collection.return_value.find.return_value.batch_size.return_value = [
            self.fake_errata,
        ]

        migration.migrate()

        self.assertEqual(mock_get_collection.call_count, 1)
        mock_get_collection.return_value.update.assert_called_with(
            {'_id': self.fake_errata['_id']},
            {'$set': {'relogin_suggested': ''}})
        mock_get_collection.return_value.update.assert_called_with(
            {'_id': self.fake_errata['_id']},
            {'$set': {'restart_suggested': ''}})