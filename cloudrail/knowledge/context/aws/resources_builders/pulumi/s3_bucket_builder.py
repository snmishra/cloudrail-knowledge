from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_s3_bucket, \
    build_s3_access_point, build_s3_acl, build_s3_public_access_block_settings, build_s3_bucket_encryption, \
    build_s3_bucket_object, build_s3_bucket_versioning, build_s3_bucket_logging
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import PublicAccessBlockLevel


class S3BucketBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_bucket(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET


class S3AccessPointBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_access_point(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_ACCESS_POINT


class S3AclBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_acl(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET


class PublicAccessBlockSettingsBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        attributes["tf_res_type"] = self.get_service_name()
        return build_s3_public_access_block_settings(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET_PUBLIC_ACCESS_BLOCK


class AccountPublicAccessBlockSettingsBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        attributes["access_level"] = PublicAccessBlockLevel.ACCOUNT
        attributes["tf_res_type"] = self.get_service_name()
        return build_s3_public_access_block_settings(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_ACCOUNT_PUBLIC_ACCESS_BLOCK


class S3BucketEncryptionBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_bucket_encryption(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET


class S3BucketObjectBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_bucket_object(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET_OBJECT


class S3BucketVersioningBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_bucket_versioning(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET


class S3BucketLoggingBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_s3_bucket_logging(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET
