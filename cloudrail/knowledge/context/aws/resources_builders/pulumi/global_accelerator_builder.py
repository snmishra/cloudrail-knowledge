from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_global_accelerator, build_global_accelerator_listener, \
    build_global_accelerator_endpoint_group, build_global_accelerator_attribute
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlobalAcceleratorBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_global_accelerator(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLOBALACCELERATOR_ACCELERATOR


class GlobalAcceleratorListenerBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_global_accelerator_listener(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLOBALACCELERATOR_LISTENER


class GlobalAcceleratorEndpointGroupBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_global_accelerator_endpoint_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLOBALACCELERATOR_ENDPOINT_GROUP


class GlobalAcceleratorAttributeBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_global_accelerator_attribute(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLOBALACCELERATOR_ACCELERATOR
