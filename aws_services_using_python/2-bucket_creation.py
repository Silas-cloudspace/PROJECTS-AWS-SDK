import boto3

# Create a boto3 resource for S3 and name your bucket
s3 = boto3.resource('s3')
bucket_name = 'st-crud-1'
region = 'eu-west-2'  # Replace with the desired region

# Check if bucket exists
# Create the bucket if it does NOT exist
all_my_buckets = [bucket.name for bucket in s3.buckets.all()]
if bucket_name not in all_my_buckets:
    print(f"'{bucket_name}' bucket does not exist. Creating now...")
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region}
    )
    print(f"'{bucket_name}' bucket has been created.")
else:
    print(f"'{bucket_name}' bucket already exists. No need to create a new one.")