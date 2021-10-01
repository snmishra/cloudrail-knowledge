from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_ecr_repository


class EcrRepositoryBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_ecr_repository(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ECR_REPOSITORY
