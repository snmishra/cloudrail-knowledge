from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_s3_policy, \
    build_managed_policy, build_inline_s3_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class S3BucketPolicyBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET_POLICY

class S3BucketInlinePolicyBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_inline_s3_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET



class ManagedPolicyBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_managed_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_POLICY
