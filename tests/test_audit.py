import unittest
from unittest.mock import Mock
from audit_rds import evaluate_instance, audit_rds_instances

class RDSTests(unittest.TestCase):
    def test_fields_do_not_infer_private_subnets(self):
        result = evaluate_instance({"DBInstanceIdentifier": "demo",
                                    "StorageEncrypted": True,
                                    "PubliclyAccessible": False})
        self.assertTrue(result["encrypted"])
        self.assertFalse(result["publicly_accessible"])
        self.assertNotIn("private_subnet", result)

    def test_pagination_and_empty_account(self):
        client = Mock()
        client.get_paginator.return_value.paginate.return_value = [
            {"DBInstances": []}, {"DBInstances": [{"DBInstanceIdentifier": "later"}]}]
        self.assertEqual(audit_rds_instances(client)[0]["identifier"], "later")
        client.get_paginator.assert_called_once_with("describe_db_instances")
        client.get_paginator.return_value.paginate.return_value = [{"DBInstances": []}]
        self.assertEqual(audit_rds_instances(client), [])
