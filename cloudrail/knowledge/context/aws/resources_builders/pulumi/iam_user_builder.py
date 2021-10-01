from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_policy_user_attachment, build_iam_user, \
    build_user_inline_policy, build_iam_user_group_membership, build_user_login_profile
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamUserBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_iam_user(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER


class PolicyUserAttachmentBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_policy_user_attachment(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_POLICY_ATTACHMENT


class UserInlinePolicieBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_user_inline_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_POLICY


class IamUserGroupMembershipBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_iam_user_group_membership(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_GROUP_MEMBERSHIP


class IamUsersLoginProfileBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_user_login_profile(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_LOGIN_PROFILE
