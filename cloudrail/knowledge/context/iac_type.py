from enum import Enum


class IacType(str, Enum):
    TERRAFORM = 'terraform'
    CLOUDFORMATION = 'cloudformation'
    PULUMI = 'pulumi'

    @staticmethod
    def to_string(iac_type: 'IacType') -> str:
        iac_type_str: str = ''
        if iac_type == IacType.TERRAFORM:
            iac_type_str = 'Terraform'
        elif iac_type == IacType.CLOUDFORMATION:
            iac_type_str = 'CloudFormation'
        elif iac_type == IacType.PULUMI:
            iac_type_str = 'Pulumi'
        return iac_type_str
