import boto3
import json

def create_api(api_name, api_gateway):
    response = api_gateway.create_rest_api(
        name=api_name,
        description='API for Coffee Shop',
    )
    
    return response['id']

def create_resource_and_methods(api_id, resource_path, api_gateway, function_names, lambda_client):
    root_resource_id = api_gateway.get_resources(restApiId=api_id)['items'][0]['id']

    resource_response = api_gateway.create_resource(
        restApiId=api_id,
        parentId=root_resource_id,
        pathPart=resource_path
    )

    resource_id = resource_response['id']

    http_methods = ['GET', 'POST', 'PUT', 'DELETE']
    for idx, http_method in enumerate(http_methods):
        function_name = function_names[idx]
        api_gateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            authorizationType='NONE'
        )
        integrate_resource_with_lambda(api_gateway, api_id, resource_id, http_method, function_name)
        add_lambda_permission(function_name, http_method, api_id, resource_path, lambda_client)

    return resource_id

def integrate_resource_with_lambda(api_gateway, api_id, resource_id, http_method, function_name):
    lambda_uri = f'arn:aws:apigateway:<your region>:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-south-2:<your aws acc id>:function:{function_name}/invocations'
    integration_response = api_gateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=http_method,
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=lambda_uri
    )
    print(f'Integration for {http_method} method and Lambda function {function_name} created!')

def add_lambda_permission(function_name, http_method, api_id, resource_path, lambda_client):
    
    # Construct the Source ARN
    api_gw_region = 'eu-south-2'  # Change to your region
    account_id = '291475423968'  # Change to your account ID
    api_gw_id = api_id
    method = http_method
    resource = resource_path
    statement_id = f'APIGatewayInvokePermission-{function_name}'
    
    source_arn = f"arn:aws:execute-api:{api_gw_region}:{account_id}:{api_gw_id}/*/{method}/{resource}"

    response = lambda_client.add_permission(
        FunctionName=function_name,
        StatementId=statement_id,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=source_arn
    )

    print(f'Lambda permission added for {function_name}')

def create_stage(api_id, stage_name, api_gateway):
    deployment_response = api_gateway.create_deployment(
        restApiId=api_id,
        stageName=stage_name
    )
    
    print(f"Deplpoyments ID: {deployment_response['id']}")