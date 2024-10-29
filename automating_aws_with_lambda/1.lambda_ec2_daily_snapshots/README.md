# AUTOMATING AWS WITH PYTHON | PART 5 : EC2 DAILY SNAPSHOTS

![Picture3](https://github.com/user-attachments/assets/002cdad7-8b4a-4b8d-a16e-259cf60f6683)

Today we are setting up an AWS infrastructure to automatically create EC2 snapshots using Python, AWS Lambda and EventBridge. The setup involves the following components:

## 1.	PREREQUISITES

### •	AWS CLI and SAM CLI Installed:

Ensure that you have the AWS CLI and SAM CLI installed on your local machine. These tools are used for interacting with AWS services and deploying SAM applications.

### •	AWS CLI

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

### •	SAM CLI

https://github.com/aws/aws-sam-cli/releases

### •	Docker:

Docker is required for local testing of Lambda functions using SAM CLI. Install Docker and ensure it’s running.

https://www.docker.com/products/docker-desktop/

### •	AWS Account:

You need an AWS account to deploy resources. Ensure you have appropriate permissions to create IAM roles, Lambda functions, EC2 instances, and EventBridge rules.

## 2.	LAMBDA FUNCTION:

Purpose: This function will be triggered to create a snapshot of an EC2 instance. It finds the volume ID of an EC2 instance based on a tag and then creates a snapshot of that volume.

Code:

•	Imports necessary libraries (boto3, logging, etc.).

•	Retrieves the EC2 instance volume ID based on a tag.

•	Creates a snapshot of the volume.

•	Logs the success or failure of the snapshot creation.

## 3.	CLOUDFORMATION TEMPLATE:

Purpose: Defines the AWS resources and configurations required for the Lambda function, EC2 instance, EventBridge rule, and necessary permissions.

Components:

•	IAM Role (LambdaExecutionRole): Grants permissions to the Lambda function to interact with EC2 and CloudWatch Logs.

•	Lambda Function (LambdaEC2DailySnapshot): The function is scheduled to run automatically.

•	EC2 Instance (EC2Instance): An example EC2 instance used for snapshot creation. You can update the AMI ID and other properties as needed.

•	EventBridge Rule (DailyEC2SnapshotRule): Schedules the Lambda function to run periodically (24 hours).

•	Lambda Permission (LambdaInvokePermission): Allows EventBridge to invoke the Lambda function.

## 4.	IAM POLICY DOCUMENT:

Purpose: Provides the permissions required by the Lambda function to create and manage EC2 snapshots and interact with CloudWatch Logs.

Permissions:

Allows logging actions (logs:CreateLogGroup, logs:CreateLogStream, etc.).

Allows EC2 actions (ec2:CreateSnapshot, ec2:DescribeSnapshots, etc.).

## 5.	PREPARING THE ENVIRONMENT

Create 3 new files on VS Code:

•	touch lambda_function.py template.yaml event.json

•	Copy the code from the GitHub repository into them

## 6.	RUN THE CODE

In command prompt run: “sam deploy --guided”




