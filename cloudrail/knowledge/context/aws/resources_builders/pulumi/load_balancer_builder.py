from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper \
    import build_load_balancer, build_load_balancer_target_group, \
    build_load_balancer_target_group_association, build_load_balancer_target
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class LoadBalancerBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_load_balancer(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER


class LoadBalancerTargetGroupBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_load_balancer_target_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER_TARGET_GROUP


class LoadBalancerTargetGroupAssociationBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_load_balancer_target_group_association(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER_LISTENER


class LoadBalancerTargetBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_load_balancer_target(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER_TARGET_GROUP_ATTACHMENT
