import boto3
import json
import time


def create_iam_role():
    iam_client = boto3.client('iam')

    role_name = "LambdaDynamoDBAPIGatewayAccess" 
    role_description = "IAM role for Lambda function to access DynamoDB and API Gateway"
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    response = iam_client.create_role(
        RoleName=role_name,
        Description=role_description,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy_document)
    )
    role_arn = response['Role']['Arn']

    # Attach the DynamoDB permission policy
    policy_arn_dynamodb = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
    response_attach_dynamodb = iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn_dynamodb
    )


# Create a policy to allow API Gateway to invoke Lambda functions
    policy_name_apigateway = "APIGatewayInvokeLambdaPolicy"
    policy_document_apigateway = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "lambda:InvokeFunction",
                "Resource": "*"
            }
        ]
    }
    response_create_policy = iam_client.create_policy(
        PolicyName=policy_name_apigateway,
        PolicyDocument=json.dumps(policy_document_apigateway)
    )
    
    # Attach the API Gateway invoke policy to the role
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=response_create_policy['Policy']['Arn']
    )

    print("IAM role created and policies attached:")
    print("Role ARN:", role_arn)
    return role_arn, role_name


def create_lambda_function(role_arn, function_name, zip_file_path):
    lambda_client = boto3.client('lambda')

    function_name = function_name
    with open(zip_file_path, 'rb') as zip_file:
        zip_file_content = zip_file.read()

    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.11',
        Role=role_arn,
        Handler=f'{function_name}.lambda_handler',
        Code={
            'ZipFile': zip_file_content
        },
        Description='Coffee Shop Lambda Function',
        Timeout=30,
        MemorySize=256
    )

    print(f"Lambda function created: {response['FunctionArn']}")


