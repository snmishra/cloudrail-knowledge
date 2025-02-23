from typing import List

from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlacierVaultPolicy(Policy):
    """
        Attributes:
            vault_arn: The ARN of the vault the policy applies to.
            policy_statements: The policy's statements.
            raw_document: The raw JSON of the policy.
    """
    def __init__(self,
                 vault_arn: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_GLACIER_VAULT)
        self.vault_arn: str = vault_arn

    def get_keys(self) -> List[str]:
        return [self.vault_arn]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'S3 Glacier Vault resource policy'
        else:
            return 'S3 Glacier Vault resource policies'
