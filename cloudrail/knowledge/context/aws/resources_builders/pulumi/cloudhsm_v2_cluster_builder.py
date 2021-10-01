from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_cloudhsm_v2_cluster_builder, build_cloudhsm_v2_hsm
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudHsmV2ClusterBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_cloudhsm_v2_cluster_builder(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDHSM_V_2_CLUSTER


class CloudHsmV2HsmBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_cloudhsm_v2_hsm(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDHSM_V_2_HSM
