import unittest

from pulp.server.db.migrate.models import _import_all_the_way
import mock

migration = _import_all_the_way('pulp_rpm.plugins.migrations.0042_add_suse_'
                                'fields_to_errata')

fake_errata = {
    '_id': 'abc123'
}


class TestMigrate(unittest.TestCase):
    """
    Test the migrate() function.
    """
    @mock.patch.object(migration, 'get_collection')
    def test_calls_correct_functions(self, mock_get_collection):
        """
        """
        mock_get_collection.return_value.find.return_value = [
            fake_errata,
        ]
        migration.migrate()

        self.assertEqual(mock_get_collection.call_count, 1)
        mock_get_collection.return_value.update.assert_called_once_with(
            {'_id': fake_errata['_id']},
            {'$set': {'relogin_suggested': '', 'restart_suggested': ''}})
