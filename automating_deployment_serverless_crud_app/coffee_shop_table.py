import boto3

def create_table():
    dynamodb = boto3.client('dynamodb')

    #Create 'CoffeeOrders' DynamoDB Table
    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'OrderId',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'CustomerName',
                'AttributeType': 'S',
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'OrderId',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'CustomerName',
                'KeyType': 'RANGE',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
        TableName='CoffeeOrders',
    )

    print('Successfully created Coffee Shop Table\n')