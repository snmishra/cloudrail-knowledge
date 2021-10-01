from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_sagemaker_notebook_instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SageMakerNotebookInstanceBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_sagemaker_notebook_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_SAGEMAKER_NOTEBOOK_INSTANCE
