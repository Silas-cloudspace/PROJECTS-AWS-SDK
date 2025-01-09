import boto3
import json
import time
import os
import coffee_shop_table
import coffee_shop_lambdas
import coffee_shop_api

api_gateway = boto3.client('apigateway')
lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

# Create Coffee Shop Table
try:
    coffee_shop_table.create_table()
except Exception as e:
    print(f"Error creating IAM role: {e}")
    raise

# Function to check if IAM role is fully deployed
def is_role_fully_deployed(role_name):
    try:
        iam_client.get_role(RoleName=role_name)
        return True
    except iam_client.exceptions.NoSuchEntityException:
        return False

# Create Coffee Shop Lambdas 
role_arn, role_name = coffee_shop_lambdas.create_iam_role()
max_attempts = 6  
attempt = 0
time.sleep(10)

while attempt < max_attempts:
    if is_role_fully_deployed(role_name):
        print("IAM role is fully deployed.")
        break
    print("Waiting for IAM role to be fully deployed...")
    time.sleep(10)
    attempt += 1

if attempt == max_attempts:
    print("Failed to deploy IAM role within the expected time.")
    raise Exception("IAM role deployment timeout.")

# Get the current directory of the Python script
current_dir = os.path.dirname(os.path.abspath(__file__))

#Set Lambda function names and get corresponding zip files to upload to AWS
zip_paths = {
    'get_order': os.path.join(current_dir, 'get_order.zip'),
    'post_order': os.path.join(current_dir, 'post_order.zip'),
    'put_order': os.path.join(current_dir, 'put_order.zip'),
    'delete_order': os.path.join(current_dir, 'delete_order.zip')
}

for key, value in zip_paths.items():
    try:
        coffee_shop_lambdas.create_lambda_function(role_arn, key, value)
    except Exception as e:
        print(f"Error creating Lambda function {key}: {e}")
        raise


# Create Coffee Shop API 
api_name = 'CoffeeShopAPI'
try:
    api_id = coffee_shop_api.create_api(api_name, api_gateway)
    print(f'API ID: {api_id}\n')
except Exception as e:
        print(f"Error creating API Gateway: {e}")
        raise


resource_path = 'Orders'
function_names = ['get_order', 'post_order', 'put_order', 'delete_order']  # Replace with your Lambda function names

try:
    resource_id = coffee_shop_api.create_resource_and_methods(api_id, resource_path, api_gateway, function_names, lambda_client)
    print(f'Resource ID for "{resource_path}": {resource_id}\n')
except Exception as e:
        print(f"Error creating Resources and Methods: {e}")
        raise

stage_name = 'Prod'
try:
    coffee_shop_api.create_stage(api_id, stage_name, api_gateway)
    print(f"API '{api_name}' with ID '{api_id}' deployed to stage '{stage_name}'.")
except Exception as e:
        print(f"Error creating Stage: {e}")
        raise