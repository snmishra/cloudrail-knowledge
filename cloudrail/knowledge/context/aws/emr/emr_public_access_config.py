from typing import List
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class EmrPublicAccessConfiguration(AwsResource):

    def __init__(self,
                 account: str,
                 region: str,
                 public_access: bool):
        super().__init__(account, region, AwsServiceName.NONE)
        self.public_access: bool = public_access

    def get_keys(self) -> List[str]:
        return [self.account, self.region]

    def get_name(self) -> str:
        return f'EMR block public access configuration for region {self.region} in account {self.account}'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}elasticmapreduce/home?region={1}#block-public-access:'\
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return False
