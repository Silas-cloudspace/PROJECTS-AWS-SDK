import boto3

def update_lambda_timeout(function_name, new_timeout):
    client = boto3.client('lambda', region_name='eu-west-2')  # Specify your region
    
    response = client.update_function_configuration(
        FunctionName=function_name,
        Timeout=new_timeout  # Timeout in seconds
    )
    
    print(f"Updated timeout for function {function_name} to {new_timeout} seconds.")
    print(response)

if __name__ == "__main__":
    function_name = 'BillingBucketParser'  # Replace with your Lambda function name
    new_timeout = 30  # Set the new timeout value in seconds
    
    update_lambda_timeout(function_name, new_timeout)
