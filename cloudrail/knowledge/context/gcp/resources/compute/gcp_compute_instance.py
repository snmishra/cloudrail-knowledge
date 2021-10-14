from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_health_check import GcpComputeHealthCheck


class GcpComputeInstanceBootDiskMode(Enum):
    READ_WRITE = 'READ_WRITE'
    READ_ONLY = 'READ_ONLY'

class GcpComputeInstanceBootDiskInitPraramsType(Enum):
    PD_STANDARD = 'pd-standard'
    PD_BALANCED = 'pd-balanced'
    PD_SSD = 'pd-ssd'

class GcpComputeInstanceAttachDiskMode(Enum):
    READ_WRITE = 'READ_WRITE'
    READ_ONLY = 'READ_ONLY'

class GcpComputeInstanceNetIntfNicType(Enum):
    GVNIC  = 'gvnic'
    VIRTIO_NET = 'virtio_net'

@dataclass
class GcpComputeInstanceBootDiskInitPrarams:
    """
        Attributes:
            size:(Optional) The size of the image in gigabytes.
            type: (Optional) The GCE disk type. May be set to pd-standard, pd-balanced or pd-ssd.
            image: (Optional) The image from which to initialize this disk.
    """
    size: Optional[float]
    type: Optional[GcpComputeInstanceBootDiskInitPraramsType]
    image: Optional[str]


@dataclass
class GcpComputeInstanceBootDisk:
    """
        Attributes:
            auto_delete: (Optional) Whether the disk will be auto-deleted when the instance is deleted.
            device_name: (Optional) Name with which attached disk will be accessible.
            mode: (Optional) The mode in which to attach this disk, either READ_WRITE or READ_ONLY.
            disk_encryption_key_raw: (Optional) A 256-bit [customer-supplied encryption key]
            kms_key_self_link: (Optional) The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk.
            initialize_params: (Optional) Parameters for a new disk that will be created alongside the new instance.
            source: (Optional) The name or self_link of the existing disk (such as those managed by google_compute_disk) or disk image.
    """
    device_name: Optional[str]
    mode: Optional[GcpComputeInstanceBootDiskMode]
    disk_encryption_key_raw: Optional[str]
    kms_key_self_link: Optional[str]
    initialize_params: Optional[GcpComputeInstanceBootDiskInitPrarams]
    source: Optional[str]
    auto_delete: Optional[bool] = True


@dataclass
class GcpComputeInstanceScratchDisk:
    """
        Attributes:
            interface: The disk interface to use for attaching this disk; either SCSI or NVME.
    """
    interface: str


@dataclass
class GcpComputeInstanceAttachedDisk:
    """
        Attributes:
            source: The name or self_link of the disk to attach to this instance.
            device_name: (Optional) Name with which the attached disk will be accessible.
            mode: (Optional) The mode in which to attach this disk, either READ_WRITE or READ_ONLY.
            disk_encryption_key_raw: (Optional) A 256-bit [customer-supplied encryption key]
            kms_key_self_link: (Optional) The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk.
    """
    source: Optional[str]
    device_name: Optional[str]
    mode: Optional[GcpComputeInstanceAttachDiskMode]
    disk_encryption_key_raw: Optional[str]
    kms_key_self_link: Optional[str]

@dataclass
class GcpComputeInstanceNetPerfCfg:
    """
        Attributes:
            total_egress_bandwidth_tier: (Optional) The egress bandwidth tier to enable. Possible values: TIER_1, DEFAULT.
    """
    total_egress_bandwidth_tier: Optional[str]


@dataclass
class GcpComputeInstanceNetIntfAccessCfg:
    """
        Attributes:
            nat_ip: (Optional) The IP address that will be 1:1 mapped to the instance's network ip.
            public_ptr_domain_name: (Optional) The DNS domain name for the public PTR record.
            network_tier: (Optional) The networking tier used for configuring this instance. Possible values: PREMIUM, STANDARD.
    """
    nat_ip: Optional[str]
    public_ptr_domain_name: Optional[str]
    network_tier: Optional[str] = 'PREMIUM'


@dataclass
class GcpComputeInstanceNetIntfAliasIpRange:
    """
        Attributes:
            ip_cidr_range: The IP CIDR range represented by this alias IP range.
            subnetwork_range_name: (Optional) The subnetwork secondary range name specifying the secondary range.
    """
    ip_cidr_range: str
    subnetwork_range_name: Optional[str]


@dataclass
class GcpComputeInstanceNetworkInterface:
    """
        Attributes:
            network: (Optional) The name or self_link of the network to attach this interface to.
            subnetwork: (Optional) The name or self_link of the subnetwork to attach this interface to.
            subnetwork_project: (Optional) The project in which the subnetwork belongs.
            network_ip: (Optional) The private IP address to assign to the instance.
            access_config: (Optional) Access configurations, i.e. IPs via which this instance can be accessed via the Internet.
            alias_ip_range: (Optional) An array of alias IP ranges for this network interface.
            nic_type: (Optional) The type of vNIC to be used on this interface. Possible values: GVNIC, VIRTIO_NET.

    """
    network: Optional[str]
    subnetwork: Optional[str]
    subnetwork_project: Optional[str]
    network_ip: Optional[str]
    access_config: Optional[List[GcpComputeInstanceNetIntfAccessCfg]]
    alias_ip_range: Optional[List[GcpComputeInstanceNetIntfAliasIpRange]]
    nic_type: Optional[GcpComputeInstanceNetIntfNicType]


@dataclass
class GcpComputeInstanceServiceAcount:
    """
        Attributes:
            email: (Optional) The service account e-mail address. If not given, the default Google Compute Engine service account is used.
            scopes: A list of service scopes. Both OAuth2 URLs and gcloud short names are supported.
    """
    email: Optional[str]
    scopes: str


@dataclass
class GcpComputeInstanceNodeAffinity:
    """
        Attributes:
            key: The key for the node affinity label.
            operator: The operator and possible values are IN for node-affinities and NOT_IN for anti-affinities.
            values: The values for the node affinity label.
    """
    key: str
    operator: str
    values: Optional[str]

@dataclass
class GcpComputeInstanceScheduling:
    """
        Attributes:
            preemptible: (Optional) Specifies if the instance is preemptible.
            on_host_maintenance: (Optional) Describes maintenance behavior for the instance. Possible values: MIGRATE, TERMINATE.
            automatic_restart: (Optional) Specifies if the instance should be restarted if it was terminated by Compute Engine (not a user).
            node_affinities: (Optional) Specifies node affinities or anti-affinities to determine hosts for sole-tenant nodes.
            min_node_cpus: (Optional) The minimum number of virtual CPUs this instance will consume when running on a sole-tenant node.
    """
    node_affinities: Optional[GcpComputeInstanceNodeAffinity]
    min_node_cpus: Optional[int]
    on_host_maintenance: Optional[str]
    preemptible: Optional[bool] = False
    automatic_restart: Optional[bool] = True

@dataclass
class GcpComputeInstanceGuestAccelerator:
    """
        Attributes:
            type: The accelerator type resource to expose to this instance. Ex: nvidia-tesla-k80.
            count: The number of the guest accelerator cards exposed to this instance.
    """
    type: str
    count: int

@dataclass
class GcpComputeInstanceShieldInstCfg:
    """
        Attributes:
            enable_secure_boot: (Optional) Verify the digital signature of all boot components, and halt the boot process on failure.
            enable_vtpm: (Optional) Use a virtualized trusted platform module, to encrypt objects like keys and certificates.
            enable_integrity_monitoring: (Optional) Compare the most recent boot measurements to the integrity policy baseline and return a pair of pass/fail results.
    """
    enable_secure_boot: Optional[bool] = False
    enable_vtpm: Optional[bool] = True
    enable_integrity_monitoring: Optional[bool] = True


@dataclass
class GcpComputeInstanceConfInstCfg:
    """
        Attributes:
            enable_confidential_compute: (Optional) Defines whether the instance should have confidential compute enabled.
    """
    enable_confidential_compute: Optional[bool]


@dataclass
class GcpComputeInstanceAdvMachineFeatures:
    """
        Attributes:
            enable_nested_virtualization: (Optional) Defines whether the instance should have nested virtualization enabled.
            threads_per_core: (Optional) The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1.
    """
    threads_per_core: Optional[int]
    enable_nested_virtualization: Optional[bool] = False


@dataclass
class GcpComputeInstanceSpecificResv:
    """
        Attributes:
            key: Corresponds to the label key of a reservation resource.
            values: Corresponds to the label values of a reservation resource.
    """
    key: str
    values: str


@dataclass
class GcpComputeInstanceResvAffinity:
    """
        Attributes:
            type: The type of reservation from which this instance can consume resources.
            specific_reservation: (Optional) Specifies the label selector for the reservation to use.
    """
    type: str
    specific_reservation: Optional[GcpComputeInstanceSpecificResv]


class GcpComputeInstance(GcpResource):
    """
        Attributes:
            boot_disk: The boot disk for the instance.
            machine_type: The machine type to create.
            name: A unique name for the compute instance.
            zone: (Optional) The zone that the machine should be created in.
            network_interfaces: Networks to attach to the instance.
            allow_stopping_for_update: ((Optional) If true, allows Terraform to stop the instance to update its properties.
            attached_disk: (Optional) (Optional) Additional disks to attach to the instance.
            can_ip_forward: (Optional) Whether to allow sending and receiving of packets with non-matching source or destination IPs.
            description: ((Optional) A brief description of this resource.
            desired_status: (Optional) Desired status of the instance.
            deletion_protection: (Optional) Enable deletion protection on this instance.
            hostname: (Optional) A custom hostname for the instance.
            guest_accelerator: (Optional) List of the type and count of accelerator cards attached to the instance.
            labels: (Optional) A map of key/value label pairs to assign to the instance.
            metadata: (Optional) Metadata key/value pairs to make available from within the instance.
            metadata_startup_script: (Optional) An alternative to using the startup-script metadata key, forces the instance to be recreated if it is changed.
            min_cpu_platform: (Optional) Specifies a minimum CPU platform for the VM instance.
            project: (Optional) The ID of the project in which the resource belongs.
            scheduling: (Optional) The scheduling strategy to use.
            scratch_disk: (Optional) Scratch disks to attach to the instance.
            service_account: (Optional) Service account to attach to the instance.
            tags: (Optional) A list of network tags to attach to the instance.
            shielded_instance_config: (Optional) Enable Shielded VM on this instance.
            enable_display: (Optional) Enable Virtual Displays on this instance.
            resource_policies: (Optional) A list of short names or self_links of resource policies to attach to the instance.
            reservation_affinity: (Optional) Specifies the reservations that this instance can consume from.
            confidential_instance_config: (Optional) - Enable Confidential Mode on this VM.
            advanced_machine_features: (Optional) Configure Nested Virtualisation and Simultaneous Hyper Threading on this VM.
            network_performance_config: (Optional, Beta Configures network performance settings for the instance.
    """
    def __init__(self,
                 boot_disk: GcpComputeInstanceBootDisk,
                 machine_type: str,
                 name: str,
                 zone: str,
                 network_interfaces: Optional[List[GcpComputeInstanceNetworkInterface]],
                 attached_disks: Optional[List[GcpComputeInstanceAttachedDisk]],
                 can_ip_forward: Optional[bool],
                 description: Optional[str],
                 desired_status: Optional[str],
                 deletion_protection: Optional[bool],
                 hostname: Optional[str],
                 guest_accelerator: Optional[List[GcpComputeInstanceGuestAccelerator]],
                 labels: Optional[List[str]],
                 metadata: Optional[List[str]],
                 metadata_startup_script: Optional[str],
                 min_cpu_platform: Optional[str],
                 project: Optional[str],
                 scheduling: Optional[GcpComputeInstanceScheduling],
                 scratch_disks: Optional[List[GcpComputeInstanceScratchDisk]],
                 service_account: Optional[GcpComputeInstanceServiceAcount],
                 shielded_instance_config: Optional[GcpComputeInstanceShieldInstCfg],
                 enable_display: Optional[bool],
                 resource_policies: Optional[List[str]],
                 reservation_affinity: Optional[GcpComputeInstanceResvAffinity],
                 confidential_instance_config: Optional[GcpComputeInstanceConfInstCfg],
                 advanced_machine_features: Optional[GcpComputeInstanceAdvMachineFeatures],
                 network_performance_config: Optional[GcpComputeInstanceNetPerfCfg]):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_INSTANCE)
        self.boot_disk: GcpComputeInstanceBootDisk = boot_disk
        self.machine_type: str = machine_type
        self.name: str = name
        self.zone: str = zone
        self.network_interfaces: Optional[List[GcpComputeInstanceNetworkInterface]] = network_interfaces
        self.attached_disks: Optional[List[GcpComputeInstanceAttachedDisk]] = attached_disks
        self.can_ip_forward: bool = can_ip_forward
        self.description: str = description
        self.desired_status: str = desired_status
        self.deletion_protection: bool = deletion_protection
        self.hostname: str = hostname
        self.guest_accelerator: Optional[List[GcpComputeInstanceGuestAccelerator]] = guest_accelerator
        self.labels: List[str] = labels
        self.metadata: List[str] = metadata
        self.metadata_startup_script: str = metadata_startup_script
        self.min_cpu_platform: Optional[str] = min_cpu_platform
        self.project: str = project
        self.scheduling: Optional[GcpComputeInstanceScheduling] = scheduling
        self.scratch_disks: Optional[List[GcpComputeInstanceScratchDisk]] = scratch_disks
        self.service_account: Optional[GcpComputeInstanceServiceAcount] = service_account
        self.shielded_instance_config: Optional[GcpComputeInstanceShieldInstCfg] = shielded_instance_config
        self.enable_display: bool = enable_display
        self.resource_policies: Optional[List[str]] = resource_policies
        self.reservation_affinity: Optional[GcpComputeInstanceResvAffinity] = reservation_affinity
        self.confidential_instance_config: Optional[GcpComputeInstanceConfInstCfg] = confidential_instance_config
        self.advanced_machine_features: Optional[GcpComputeInstanceAdvMachineFeatures] = advanced_machine_features
        self.network_performance_config: Optional[GcpComputeInstanceNetPerfCfg] = network_performance_config

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/compute/instancesDetail/zones/{self.zone}/instances/{self.name}?project={self.project}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Virtual Machine Instance'
        else:
            return 'Virtual Machine Instances'

    @property
    def is_tagable(self) -> bool:
        return True
