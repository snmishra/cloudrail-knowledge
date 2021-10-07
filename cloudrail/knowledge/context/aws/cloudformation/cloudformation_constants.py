from enum import Enum


class CloudformationResourceType(str, Enum):
    VPC = 'AWS::EC2::VPC'
    INTERNET_GATEWAY = 'AWS::EC2::InternetGateway'
    VPC_GATEWAY_ATTACHMENT = 'AWS::EC2::VPCGatewayAttachment'
    EC2_INSTANCE = 'AWS::EC2::Instance'
    SUBNET = 'AWS::EC2::Subnet'
    SECURITY_GROUP = 'AWS::EC2::SecurityGroup'
    NAT_GW = 'AWS::EC2::NatGateway'
    SECURITY_GROUP_EGRESS = 'AWS::EC2::SecurityGroupEgress'
    SECURITY_GROUP_INGRESS = 'AWS::EC2::SecurityGroupIngress'
    ROUTE_TABLE = 'AWS::EC2::RouteTable'
    ROUTE = 'AWS::EC2::Route'
    SUBNET_ROUTE_TABLE_ASSOCIATION = 'AWS::EC2::SubnetRouteTableAssociation'
    S3_BUCKET = 'AWS::S3::Bucket'
    S3_BUCKET_POLICY = 'AWS::S3::BucketPolicy'
    DAX_CLUSTER = 'AWS::DAX::Cluster'
    IAM_ROLE = 'AWS::IAM::Role'
    ATHENA_WORKGROUP = 'AWS::Athena::WorkGroup'
    KMS_KEY = 'AWS::KMS::Key'
    CLOUDTRAIL = 'AWS::CloudTrail::Trail'
    CODEBUILD_REPORTGROUP = 'AWS::CodeBuild::ReportGroup'
    ELASTIC_LOAD_BALANCER = 'AWS::ElasticLoadBalancingV2::LoadBalancer'
    ELASTIC_LOAD_BALANCER_LISTENER = 'AWS::ElasticLoadBalancingV2::Listener'
    API_GATEWAY_V2 = 'AWS::ApiGatewayV2::Api'
    API_GATEWAY_V2_VPC_LINK = 'AWS::ApiGatewayV2::VpcLink'
    API_GATEWAY_V2_INTEGRATION = 'AWS::ApiGatewayV2::Integration'
    BATCH_COMPUTE_ENVIRONMENT = 'AWS::Batch::ComputeEnvironment'
    ELASTIC_LOAD_BALANCER_TARGET_GROUP = 'AWS::ElasticLoadBalancingV2::TargetGroup'
    ELASTIC_IP = 'AWS::EC2::EIP'
    DYNAMODB_TABLE = 'AWS::DynamoDB::Table'
    CONFIG_SERVICE_AGGREGATOR = 'AWS::Config::ConfigurationAggregator'
    AUTO_SCALING_GROUP = 'AWS::AutoScaling::AutoScalingGroup'
    LAUNCH_TEMPLATE = 'AWS::EC2::LaunchTemplate'
    LAUNCH_CONFIGURATION = 'AWS::AutoScaling::LaunchConfiguration'
    CLOUDFRONT_DISTRIBUTION_LOGGING = 'AWS::CloudFront::Distribution'
    CLOUDWATCH_LOGS_DESTINATION = 'AWS::Logs::Destination'
