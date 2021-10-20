from typing import List
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceNetworkInterface, \
        GcpComputeInstanceNetIntfAccessCfg, GcpComputeInstanceNetIntfAliasIpRange, GcpComputeInstanceNetIntfNicType, GcpComputeInstanceServiceAcount, \
            GcpComputeInstanceShieldInstCfg

from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeInstanceBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-instances-list.json'

    def do_build(self, attributes: dict) -> GcpComputeInstance:

        ## Network Interfaces ##
        network_interfaces: List[GcpComputeInstanceNetworkInterface] = []
        for interface in attributes.get('networkInterfaces', []):

            nic_type = interface.get('nicType')
            if nic_type:
                nic_type = GcpComputeInstanceNetIntfNicType(nic_type)

            access_config_list: List[GcpComputeInstanceNetIntfAccessCfg] = []
            for access_config in interface.get('accessConfigs', []):
                access_config_list.append(GcpComputeInstanceNetIntfAccessCfg(nat_ip = access_config.get('natIP'),
                                                                             public_ptr_domain_name = access_config.get('publicPtrDomainName'),
                                                                             network_tier = access_config.get('networkTier')))

            aliases_ip_range: List[GcpComputeInstanceNetIntfAliasIpRange] = []
            for ip in interface.get('aliasIpRanges', []):
                aliases_ip_range.append(GcpComputeInstanceNetIntfAliasIpRange(ip_cidr_range=ip.get('ipCidrRange'),
                                                                              subnetwork_range_name=ip.get('subnetworkRangeName')))

            network_interfaces.append(GcpComputeInstanceNetworkInterface(network = interface.get('network'), subnetwork = interface.get('subnetwork'),
                                                                         subnetwork_project = interface.get('subnetwork_project'),
                                                                         network_ip = self._get_known_value(interface, 'network_ip'),
                                                                         access_config=access_config_list,
                                                                         alias_ip_range=aliases_ip_range,
                                                                         nic_type=nic_type))

        ## Service Account ##
        service_account = None
        if service_account_data := self._get_known_value(attributes, 'service_account'):
            service_account = GcpComputeInstanceServiceAcount(email=service_account_data[0].get('email'),
                                                              scopes=service_account_data[0]['scopes'])

        ## Shielded Instance Config ##
        shielded_instance_config = None
        if shielded_instance_config_data := self._get_known_value(attributes, 'shielded_instance_config'):
            shielded_instance_config = GcpComputeInstanceShieldInstCfg(self._get_known_value(shielded_instance_config_data[0], 'enable_secure_boot', False),
                                                                       self._get_known_value(shielded_instance_config_data[0], 'enable_vtpm', True),
                                                                       self._get_known_value(shielded_instance_config_data[0], 'enable_integrity_monitoring', True))

        return GcpComputeInstance(name=attributes['name'],
                                  zone=self._get_known_value(attributes, 'zone'),
                                  network_interfaces=network_interfaces,
                                  can_ip_forward=self._get_known_value(attributes, 'can_ip_forward', False),
                                  hostname=self._get_known_value(attributes, 'hostname'),
                                  metadata=self._get_known_value(attributes, 'metadata', []),
                                  project=self._get_known_value(attributes, 'project'),
                                  service_account=service_account,
                                  shielded_instance_config=shielded_instance_config)
