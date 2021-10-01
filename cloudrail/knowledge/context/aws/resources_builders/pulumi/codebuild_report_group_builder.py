from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_code_build_report_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CodeBuildReportGroupBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_code_build_report_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CODEBUILD_REPORT_GROUP
