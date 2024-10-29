# CRUD(Create, Read, Update. Delete) operations using boto3 and S3
import boto3

# Instantiate a boto3 resource for S3 and name your bucket
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


# Create 'file_1' and 'file_2'
file_1 = 'file_1.txt'
file_2 = 'file_2.txt'
# UPLOAD 'file_1' to the new bucket
s3.Bucket(bucket_name).upload_file(Filename=file_1, Key=file_1)


# READ and print the file from the bucket
obj = s3.Object(bucket_name, file_1)
body = obj.get()['Body'].read()
print(body)

# UPDATE 'file_1' in the bucket with new content from 'file_2'
s3.Object(bucket_name, file_1).put(Body=open(file_2, 'rb'))
obj = s3.Object(bucket_name, file_1)
body = obj.get()['Body'].read()
print(body)

# DELETE the file from the bucket
s3.Object(bucket_name, file_1).delete()


# DELETE the bucket (the bucket should be empty.)
bucket = s3.Bucket(bucket_name)
bucket.delete()
