import boto3

# Initialize S3 resource
s3 = boto3.resource("s3")

# Define bucket names and region
bucket_name1 = "dct-billing-st"
bucket_name2 = "dct-billing-errors-st"
region = "eu-west-2"

# Lists all my s3 byckets
all_my_buckets = [bucket.name for bucket in s3.buckets.all()]

# Check if first bucket exists and create it if not
if bucket_name1 not in all_my_buckets:
    print(f"'{bucket_name1}' bucket does not exist. Creating now...")
    s3.create_bucket(
        Bucket=bucket_name1,
        CreateBucketConfiguration={"LocationConstraint": region}
    )
    print(f"'{bucket_name1}' bucket has been created.")
else:
    print(f"'{bucket_name1}' bucket already exists.")

# Check if second bucket exists and create it if not
if bucket_name2 not in all_my_buckets:
    print(f"'{bucket_name2}' bucket does not exist. Creating now...")
    s3.create_bucket(
        Bucket=bucket_name2,
        CreateBucketConfiguration={"LocationConstraint": region}
    )
    print(f"'{bucket_name2}' bucket has been created.")
else:
    print(f"'{bucket_name2}' bucket already exists.")