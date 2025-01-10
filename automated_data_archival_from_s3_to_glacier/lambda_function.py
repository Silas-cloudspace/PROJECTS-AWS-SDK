import boto3
import os
from datetime import datetime, timezone, timedelta

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    threshold_days = 90  # Days to check for archival
    
    # Calculate threshold date
    threshold_date = datetime.now(timezone.utc) - timedelta(days=threshold_days)
    
    # List objects in the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print('No objects found in the bucket.')
            return
    except Exception as e:
        print(f"Failed to list objects in bucket {bucket_name}: {str(e)}")
        return
    
    for obj in response['Contents']:
        last_modified = obj['LastModified']
        key = obj['Key']
        
        # Check if the object is older than the threshold date
        if last_modified < threshold_date:
            try:
                # Overwrite object with Glacier Deep Archive storage class
                s3.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': key},
                    Key=key,
                    StorageClass='DEEP_ARCHIVE'
                )
                print(f"Archived {key} to Glacier Deep Archive.")
            except Exception as e:
                print(f"Failed to archive {key} to Glacier Deep Archive: {str(e)}")
        else:
            print(f"{key} is not older than {threshold_days} days. Skipping.")
