from typing import List
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceBootDisk, \
    GcpComputeInstanceBootDiskMode, GcpComputeInstanceBootDiskInitPrarams, GcpComputeInstanceBootDiskInitPraramsType, GcpComputeInstanceNetworkInterface, \
        GcpComputeInstanceNetIntfAccessCfg, GcpComputeInstanceNetIntfAliasIpRange, GcpComputeInstanceNetIntfNicType, GcpComputeInstanceAttachedDisk, \
            GcpComputeInstanceAttachDiskMode, GcpComputeInstanceGuestAccelerator, GcpComputeInstanceScheduling, GcpComputeInstanceNodeAffinity, \
                GcpComputeInstanceScratchDisk, GcpComputeInstanceServiceAcount, GcpComputeInstanceShieldInstCfg, GcpComputeInstanceResvAffinity, \
                    GcpComputeInstanceSpecificResv, GcpComputeInstanceConfInstCfg, GcpComputeInstanceAdvMachineFeatures, GcpComputeInstanceNetPerfCfg

from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeInstanceBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-instances-list.json'

    def do_build(self, attributes: dict) -> GcpComputeInstance:
        ## Boot disk params ##
        boot_disk_attr: dict = attributes['boot_disk'][0]
        
        boot_disk_mode = GcpComputeInstanceBootDiskMode.READ_WRITE
        if mode := self._get_known_value(boot_disk_attr, 'mode'):
            boot_disk_mode = GcpComputeInstanceBootDiskMode(mode)
        
        initialize_params = None
        if initialize_params := self._get_known_value(boot_disk_attr, 'initialize_params'):
            GcpComputeInstanceBootDiskInitPrarams(size=self._get_known_value(initialize_params[0], 'size'),
                                                  type=GcpComputeInstanceBootDiskInitPraramsType(self._get_known_value(initialize_params[0], 'size',
                                                                                                                      GcpComputeInstanceBootDiskInitPraramsType.PD_STANDARD)),
                                                  image=self._get_known_value(initialize_params[0], 'image'))
        boot_disk = GcpComputeInstanceBootDisk(device_name=self._get_known_value(boot_disk_attr, 'device_name'),
                                               mode=boot_disk_mode,
                                               disk_encryption_key_raw=self._get_known_value(boot_disk_attr, 'disk_encryption_key_raw'),
                                               kms_key_self_link=self._get_known_value(boot_disk_attr, 'disk_encryption_key_raw'),
                                               initialize_params=initialize_params, source=boot_disk_attr.get('source'))

        ## Network Interfaces ##
        network_interfaces: List[GcpComputeInstanceNetworkInterface] = []
        for interface in self._get_known_value(attributes, 'network_interface', []):

            nic_type = self._get_known_value(interface, 'nic_type')
            if nic_type:
                nic_type = GcpComputeInstanceNetIntfNicType(nic_type)

            access_config_list: List[GcpComputeInstanceNetIntfAccessCfg] = []
            for access_config in self._get_known_value(interface, 'access_config', []):
                access_config_list.append(GcpComputeInstanceNetIntfAccessCfg(nat_ip = self._get_known_value(access_config, 'nat_ip'),
                                                                             public_ptr_domain_name = self._get_known_value(access_config, 'public_ptr_domain_name'),
                                                                             network_tier = self._get_known_value(access_config, 'network_tier', 'PREMIUM')))

            aliases_ip_range: List[GcpComputeInstanceNetIntfAliasIpRange] = []
            for ip in self._get_known_value(interface, 'alias_ip_range', []):
                aliases_ip_range.append(GcpComputeInstanceNetIntfAliasIpRange(ip_cidr_range=self._get_known_value(ip, 'ip_cidr_range'),
                                                                              subnetwork_range_name=self._get_known_value(ip, 'subnetwork_range_name')))

            network_interfaces.append(GcpComputeInstanceNetworkInterface(network = interface.get('network'), subnetwork = interface.get('subnetwork'),
                                                                         subnetwork_project = interface.get('subnetwork_project'),
                                                                         network_ip = self._get_known_value(interface, 'network_ip'),
                                                                         access_config=access_config_list,
                                                                         alias_ip_range=aliases_ip_range,
                                                                         nic_type=nic_type))

        ## Attached disk ##
        attached_disks: List[GcpComputeInstanceAttachedDisk] = []
        for disk in self._get_known_value(attributes, 'attached_disk', []):
            attached_disks.append(GcpComputeInstanceAttachedDisk(source=disk['source'], device_name=self._get_known_value(disk, 'device_name'),
                                                                 mode=GcpComputeInstanceAttachDiskMode(self._get_known_value(disk, 'mode', 'READ_WRITE')),
                                                                 disk_encryption_key_raw=self._get_known_value(disk, 'disk_encryption_key_raw'),
                                                                 kms_key_self_link=self._get_known_value(disk, 'kms_key_self_link')))

        ## Guest Accelerator ##
        guest_accelerator: List[GcpComputeInstanceGuestAccelerator] = []
        for accelerator_data in self._get_known_value(attributes, 'guest_accelerator', []):
            guest_accelerator.append(GcpComputeInstanceGuestAccelerator(accelerator_data['type'],
                                                                        accelerator_data['count']))

        ## Scheduling ##
        scheduling: GcpComputeInstanceScheduling = None
        if scheduling_data := self._get_known_value(attributes, 'scheduling'):
            node_affinities = None
            node_affinities_data = self._get_known_value(scheduling_data, 'node_affinities')
            if node_affinities_data:
                node_affinities = GcpComputeInstanceNodeAffinity(key=node_affinities_data['key'],
                                                                 operator=node_affinities_data['operator'],
                                                                 values=node_affinities_data['values'])
            scheduling = GcpComputeInstanceScheduling(node_affinities=node_affinities,
                                                      min_node_cpus=self._get_known_value(scheduling_data, 'min_node_cpus'),
                                                      on_host_maintenance=self._get_known_value(scheduling_data, 'on_host_maintenance'),
                                                      preemptible=self._get_known_value(scheduling_data, 'preemptible', False),
                                                      automatic_restart=self._get_known_value(scheduling_data, 'automatic_restart', True))

        ## Scratch Disks ##
        scratch_disks: List[GcpComputeInstanceScratchDisk] = []
        for disk in self._get_known_value(attributes, 'scratch_disk', []):
            scratch_disks.append(GcpComputeInstanceScratchDisk(disk['interface']))

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

        ## Reservation Affinity ##
        reservation_affinity = None
        if reservation_affinity_data := self._get_known_value(attributes, 'reservation_affinity'):
            specific_reservation = None
            if specific_reservation_data := self._get_known_value(reservation_affinity_data[0], 'specific_reservation'):
                specific_reservation = GcpComputeInstanceSpecificResv(specific_reservation_data[0]['key'],
                                                                      specific_reservation_data[0]['values'])
            reservation_affinity = GcpComputeInstanceResvAffinity(type=reservation_affinity_data[0]['type'],
                                                                  specific_reservation=specific_reservation)

        ## Confidential Instance Config ##
        confidential_instance_config = None
        if confidential_instance_config_data := self._get_known_value(attributes, 'confidential_instance_config'):
            confidential_instance_config = GcpComputeInstanceConfInstCfg(self._get_known_value(confidential_instance_config_data[0],
                                                                                               'enable_confidential_compute'))

        ## Advanced Machine Features ##
        advanced_machine_features = None
        if advanced_machine_features_data := self._get_known_value(attributes, 'advanced_machine_features'):
            advanced_machine_features = GcpComputeInstanceAdvMachineFeatures(self._get_known_value(advanced_machine_features_data[0], 'threads_per_core'),
                                                                             self._get_known_value(advanced_machine_features_data[0], 'enable_nested_virtualization', False))

        ## Network Performance Config ##
        network_performance_config = None
        if network_performance_config_data := self._get_known_value(attributes, 'network_performance_config'):
            network_performance_config = GcpComputeInstanceNetPerfCfg(self._get_known_value(network_performance_config_data[0], 'total_egress_bandwidth_tier'))

        return GcpComputeInstance(boot_disk=boot_disk,
                                  machine_type=attributes['machine_type'],
                                  name=attributes['name'],
                                  zone=self._get_known_value(attributes, 'zone'),
                                  network_interfaces=network_interfaces,
                                  attached_disks=attached_disks,
                                  can_ip_forward=self._get_known_value(attributes, 'can_ip_forward', False),
                                  description=self._get_known_value(attributes, 'description'),
                                  desired_status=self._get_known_value(attributes, 'desired_status'),
                                  deletion_protection=self._get_known_value(attributes, 'deletion_protection'),
                                  hostname=self._get_known_value(attributes, 'hostname'),
                                  guest_accelerator=guest_accelerator,
                                  labels=self._get_known_value(attributes, 'labels', []),
                                  metadata=self._get_known_value(attributes, 'metadata', []),
                                  metadata_startup_script=self._get_known_value(attributes, 'metadata_startup_script'),
                                  min_cpu_platform=self._get_known_value(attributes, 'min_cpu_platform'),
                                  project=self._get_known_value(attributes, 'project'),
                                  scheduling=scheduling,
                                  scratch_disks=scratch_disks,
                                  service_account=service_account,
                                  shielded_instance_config=shielded_instance_config,
                                  enable_display=self._get_known_value(attributes, 'enable_display'),
                                  resource_policies=self._get_known_value(attributes, 'resource_policies', []),
                                  reservation_affinity=reservation_affinity,
                                  confidential_instance_config=confidential_instance_config,
                                  advanced_machine_features=advanced_machine_features,
                                  network_performance_config=network_performance_config)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_INSTANCE
