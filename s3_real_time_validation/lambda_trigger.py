import boto3
import json

def add_s3_trigger_to_lambda(bucket_name, lambda_arn):
    s3_client = boto3.client('s3', region_name='eu-west-2')
    
    notification_configuration = {
        "LambdaFunctionConfigurations": [
            {
                "Events": ["s3:ObjectCreated:Put"],
                "LambdaFunctionArn": lambda_arn
            }
        ]
    }
    
    try:
        # Attach the S3 bucket notification configuration to trigger the Lambda function
        response = s3_client.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration=notification_configuration
        )
        print(f"Successfully added trigger to bucket {bucket_name}.")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error adding S3 trigger: {str(e)}")

def add_s3_permission_to_lambda(lambda_function_arn, bucket_name):
    lambda_client = boto3.client('lambda', region_name='eu-west-2')

    try:
        # Remove existing permissions with the same statement ID if they exist
        lambda_client.remove_permission(
            FunctionName=lambda_function_arn,
            StatementId='AllowS3InvokePermission'
        )
    except lambda_client.exceptions.ResourceNotFoundException:
        # Permission does not exist, continue
        pass

    try:
        # Add a new permission for the Lambda function to be invoked by S3
        response = lambda_client.add_permission(
            FunctionName=lambda_function_arn,
            StatementId='AllowS3InvokePermission',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{bucket_name}'
        )
        print(f"Permission added to Lambda function {lambda_function_arn}.")
        print(response)
    except Exception as e:
        print(f"Error adding permission to Lambda function: {str(e)}")

if __name__ == "__main__":
    bucket_name = 'dct-billing-st'  # Replace with your S3 bucket name
    lambda_arn = 'arn:aws:lambda:eu-west-2:381491868231:function:BillingBucketParser'  # Replace with your Lambda ARN

    add_s3_trigger_to_lambda(bucket_name, lambda_arn)
    add_s3_permission_to_lambda(lambda_arn, bucket_name)
