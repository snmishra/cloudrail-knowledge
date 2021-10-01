from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_glacier_vault_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlacierVaultPolicyBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_glacier_vault_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLACIER_VAULT
