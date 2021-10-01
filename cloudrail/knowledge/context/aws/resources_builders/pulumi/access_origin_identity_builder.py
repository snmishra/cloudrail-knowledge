from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import origin_access_identity_builder
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class OriginAccessIdentityBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return origin_access_identity_builder(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDFRONT_ORIGIN_ACCESS_IDENTITY
