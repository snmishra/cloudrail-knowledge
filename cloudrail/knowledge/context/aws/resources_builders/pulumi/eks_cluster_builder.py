from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_eks_cluster
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class EksClusterBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_eks_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_EKS_CLUSTER
