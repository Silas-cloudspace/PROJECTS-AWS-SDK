import boto3

def update_lambda_function():
    # Initialize a session using your AWS credentials
    client = boto3.client('lambda', region_name='eu-west-2')  # Use your region

    # Read the .zip file containing your Lambda function code
    with open('lambda_function.zip', 'rb') as f:
        zip_code = f.read()

    # Update the Lambda function code
    response = client.update_function_code(
        FunctionName='BillingBucketParser',
        ZipFile=zip_code
    )

    # Print the response to confirm the update
    print(response)

if __name__ == "__main__":
    update_lambda_function()
