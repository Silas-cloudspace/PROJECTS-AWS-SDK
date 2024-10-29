import boto3

# List s3 buckets from aws
s3 = boto3.resource("s3")

for bucket in s3.buckets.all():
  print(bucket.name)