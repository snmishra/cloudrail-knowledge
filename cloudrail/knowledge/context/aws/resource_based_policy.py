from typing import List
from cloudrail.knowledge.context.aws.iam.policy import Policy, PolicyType
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class ResourceBasedPolicy(Policy):

    def __init__(self,
                 account: str,
                 statements: List[PolicyStatement],
                 raw_document: str = None,
                 aws_service_name: AwsServiceName = AwsServiceName.AWS_IAM_POLICY,
                 policy_type: PolicyType = PolicyType.RESOURCE_POLICY):
        super().__init__(account, statements, raw_document, aws_service_name, policy_type)

    @staticmethod
    def is_standalone() -> bool:
        return False
