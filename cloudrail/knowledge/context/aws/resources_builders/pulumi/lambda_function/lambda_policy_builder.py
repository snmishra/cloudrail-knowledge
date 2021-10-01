from cloudrail.knowledge.context.aws.resources.lambda_.lambda_policy import LambdaPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName

from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_lambda_policy


class LambdaPolicyBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> LambdaPolicy:
        return build_lambda_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LAMBDA_PERMISSION
