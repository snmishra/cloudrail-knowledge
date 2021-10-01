from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_lambda_function


class LambdaFunctionBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> LambdaFunction:
        return build_lambda_function(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LAMBDA_FUNCTION
