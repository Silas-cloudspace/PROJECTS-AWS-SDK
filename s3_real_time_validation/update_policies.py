import boto3

def attach_policy_to_role(role_name, policy_arn):
    iam_client = boto3.client('iam', region_name='eu-west-2')

    try:
        # Attach the predefined AmazonS3FullAccess policy
        response = iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(f"Policy {policy_arn} attached to role {role_name}.")
        print(response)
    except Exception as e:
        print(f"Error attaching policy: {str(e)}")

def add_s3_permission_to_lambda(lambda_function_arn, bucket_name):
    lambda_client = boto3.client('lambda', region_name='eu-west-2')

    try:
        # Add permission to the Lambda function to allow S3 to invoke it
        response = lambda_client.add_permission(
            FunctionName=lambda_function_arn,
            StatementId='AllowS3InvokePermission',  # Unique ID for the policy statement
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{bucket_name}'
        )
        print(f"Permission added to Lambda function {lambda_function_arn}.")
        print(response)
    except Exception as e:
        print(f"Error adding permission to Lambda function: {str(e)}")

if __name__ == "__main__":
    role_name = 'BillingBucketParser-role-1ajyc6l6'  # Replace with your IAM role name
    policy_arn = 'arn:aws:iam::aws:policy/AmazonS3FullAccess'
    lambda_function_arn = 'arn:aws:lambda:eu-west-2:381491868231:function:BillingBucketParser'  # Replace with your Lambda ARN
    bucket_name = 'dct-billing-st'  # Replace with your S3 bucket name

    attach_policy_to_role(role_name, policy_arn)
    add_s3_permission_to_lambda(lambda_function_arn, bucket_name)
