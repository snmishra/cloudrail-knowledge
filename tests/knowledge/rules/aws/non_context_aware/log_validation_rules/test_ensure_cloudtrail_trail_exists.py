import unittest

from cloudrail.knowledge.context.aws.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aws.account.account import Account
from src.ensure_cloudtrail_trail_exists import EnsureCloudtrailTrailExists

class TestEnsureCloudtrailTrailExists(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudtrailTrailExists()

    def test_ensure_cloudtrail_trail_exists_fail(self):
        # Arrange
        context = AwsEnvironmentContext()
        account_one = Account("77465564674","account", False)
        context.accounts.append(account_one)

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_ensure_cloudtrail_trail_exists_pass(self):
        # Arrange
        context = AwsEnvironmentContext()

        cloudtrail_trail = CloudTrail("trail",False,"any",False,"region","account",True)
        context.cloudtrail.append(cloudtrail_trail)

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))