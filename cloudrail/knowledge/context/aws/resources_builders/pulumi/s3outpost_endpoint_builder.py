from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_s3outpost_endpoint
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class S3OutpostEndpointBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_s3outpost_endpoint(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S_3_OUTPOSTS_ENDPOINT
