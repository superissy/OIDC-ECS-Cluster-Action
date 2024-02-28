import json
import boto3
import re

# Specify desired resource types to validate
APPLICABLE_RESOURCES = [
    "AWS::ACM::Certificate",
    "AWS::ApiGateway::RestApi",
    "AWS::ApiGateway::Stage",
    "AWS::ApiGatewayV2::Api",
    "AWS::ApiGatewayV2::Stage",
    "AWS::AutoScaling::AutoScalingGroup",
    "AWS::AutoScaling::LaunchConfiguration",
    "AWS::Backup::BackupPlan",
    "AWS::Backup::BackupSelection",
    "AWS::Backup::BackupVault",
    "AWS::CloudFormation::Stack",
    "AWS::CloudFront::Distribution",
    "AWS::CloudFront::StreamingDistribution",
    "AWS::CloudTrail::Trail",
    "AWS::CodeBuild::Project",
    "AWS::CodePipeline::Pipeline",
    "AWS::DynamoDB::Table",
    "AWS::EC2::CustomerGateway",
    "AWS::EC2::EgressOnlyInternetGateway",
    "AWS::EC2::EIP",
    "AWS::EC2::Instance",
    "AWS::EC2::InternetGateway",
    "AWS::EC2::NatGateway",
    "AWS::EC2::NetworkAcl",
    "AWS::EC2::NetworkInterface",
    "AWS::EC2::RegisteredHAInstance",
    "AWS::EC2::RouteTable",
    "AWS::EC2::SecurityGroup",
    "AWS::EC2::Subnet",
    "AWS::EC2::Volume",
    "AWS::EC2::VPC",
    "AWS::EC2::VPCEndpoint",
    "AWS::EC2::VPCEndpointService",
    "AWS::EC2::VPCPeeringConnection",
    "AWS::EC2::VPNConnection",
    "AWS::EC2::VPNGateway",
    "AWS::ECR::Repository",
    "AWS::ECS::Cluster",
    "AWS::ECS::Service",
    "AWS::ECS::TaskDefinition",
    "AWS::EFS::AccessPoint",
    "AWS::EFS::FileSystem",
    "AWS::EKS::Cluster",
    "AWS::ElasticBeanstalk::Application",
    "AWS::ElasticBeanstalk::ApplicationVersion",
    "AWS::ElasticBeanstalk::Environment",
    "AWS::ElasticLoadBalancing::LoadBalancer",
    "AWS::ElasticLoadBalancingV2::LoadBalancer",
    "AWS::Elasticsearch::Domain",
    "AWS::IAM::Group",
    "AWS::IAM::Policy",
    "AWS::IAM::Role",
    "AWS::IAM::User",
    "AWS::KMS::Key",
    "AWS::Lambda::Function",
    "AWS::NetworkFirewall::Firewall",
    "AWS::NetworkFirewall::FirewallPolicy",
    "AWS::NetworkFirewall::RuleGroup",
    "AWS::OpenSearch::Domain",
    "AWS::QLDB::Ledger",
    "AWS::RDS::DBCluster",
    "AWS::RDS::DBClusterSnapshot",
    "AWS::RDS::DBInstance",
    "AWS::RDS::DBSecurityGroup",
    "AWS::RDS::DBSnapshot",
    "AWS::RDS::DBSubnetGroup",
    "AWS::RDS::EventSubscription",
    "AWS::Redshift::Cluster",
    "AWS::Redshift::ClusterParameterGroup",
    "AWS::Redshift::ClusterSecurityGroup",
    "AWS::Redshift::ClusterSnapshot",
    "AWS::Redshift::ClusterSubnetGroup",
    "AWS::Redshift::EventSubscription",
    "AWS::S3::AccountPublicAccessBlock",
    "AWS::S3::Bucket",
    "AWS::SecretsManager::Secret",
    "AWS::ServiceCatalog::CloudFormationProduct",
    "AWS::ServiceCatalog::CloudFormationProvisionedProduct",
    "AWS::ServiceCatalog::Portfolio",
    "AWS::Shield::Protection",
    "AWS::ShieldRegional::Protection",
    "AWS::SNS::Topic",
    "AWS::SQS::Queue",
    "AWS::WAF::RateBasedRule",
    "AWS::WAF::Rule",
    "AWS::WAF::RuleGroup",
    "AWS::WAFRegional::RateBasedRule",
    "AWS::WAFRegional::Rule",
    "AWS::WAFRegional::RuleGroup",
    "AWS::WAFv2::IPSet",
    "AWS::WAFv2::RuleGroup"
]

PRODUCT_ID_PATTERN = r"^[1-9]\d{4}$"

# Function to find any violations of tag requirements
def find_violation(current_tags, required_tags):
    violation = ""
    for rtag, rvalues in required_tags.items():
        tag_present = False
        for ctag, cvalues in current_tags.items():
            if ctag == rtag:
                value_match = False
                tag_present = True
                rvaluesplit = rvalues.split(",")
                for rvalue in rvaluesplit:
                    if ctag == "product_id":
                        if re.match(PRODUCT_ID_PATTERN, str(cvalues)):
                            value_match = True
                    else:
                        if cvalues == rvalue or (cvalues != "" and rvalue == "*"):
                            value_match = True
                if not value_match:
                    violation += f"\n{ctag} value incorrect."
        if not tag_present:
            violation += f"\nTag {rtag} missing."
    return violation if violation else None

# Function to evaluate compliance of a resource
def evaluate_compliance(configuration_item, rule_parameters):
    if configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        return {
            "compliance_type": "NOT_APPLICABLE",
            "annotation": f"The rule doesn’t apply to resources of type {configuration_item['resourceType']}."
        }
    if configuration_item["configurationItemStatus"] == "ResourceDeleted":
        return {
            "compliance_type": "NOT_APPLICABLE",
            "annotation": "The configurationItem was deleted and therefore cannot be validated."
        }
    current_tags = configuration_item.get("tags")
    violation = find_violation(current_tags, rule_parameters)
    if violation:
        return {
            "compliance_type": "NON_COMPLIANT",
            "annotation": violation
        }
    return {
        "compliance_type": "COMPLIANT",
        "annotation": "This resource is compliant with the rule."
    }

# Lambda function handler
def lambda_handler(event, context):
    invoking_event = json.loads(event["invokingEvent"])
    configuration_item = invoking_event["configurationItem"]
    rule_parameters = json.loads(event["ruleParameters"])
    print(event)  # Logging the event for debugging
    result_token = event.get("resultToken", "No token found.")
    evaluation = evaluate_compliance(configuration_item, rule_parameters)
    config = boto3.client("config")
    config.put_evaluations(
        Evaluations=[
            {
                "ComplianceResourceType": configuration_item["resourceType"],
                "ComplianceResourceId": configuration_item["resourceId"],
                "ComplianceType": evaluation["compliance_type"],
                "Annotation": evaluation["annotation"],
                "OrderingTimestamp": configuration_item["configurationItemCaptureTime"]
            },
        ],
        ResultToken=result_token
    )
