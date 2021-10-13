from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance

from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder


class GcpComputeInstanceBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeInstance:
        return None
        # return GcpComputeInstance(attributes['boot_disk'],
        #                           attributes['machine_type'],
        #                           attributes['name'],
        #                           )

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_INSTANCE
