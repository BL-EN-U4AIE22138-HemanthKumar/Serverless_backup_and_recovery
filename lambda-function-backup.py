import boto3
import json
import time

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    backup_suffix = f"-backup-{int(time.time())}"
    
    try:
        # List all buckets
        response = s3_client.list_buckets()
        source_buckets = [bucket['Name'] for bucket in response['Buckets']]
        backed_up_buckets = []
        
        for source_bucket in source_buckets:
            if not source_bucket.endswith('-backup'):  # Skip backup buckets
                # Create backup bucket
                backup_bucket_name = f"{source_bucket}{backup_suffix}"
                s3_client.create_bucket(Bucket=backup_bucket_name)
                
                # Copy objects
                paginator = s3_client.get_paginator('list_objects_v2')
                for page in paginator.paginate(Bucket=source_bucket):
                    if 'Contents' in page:
                        for obj in page['Contents']:
                            copy_source = {
                                'Bucket': source_bucket,
                                'Key': obj['Key']
                            }
                            s3_client.copy_object(
                                CopySource=copy_source,
                                Bucket=backup_bucket_name,
                                Key=obj['Key']
                            )
                
                backed_up_buckets.append({
                    'source': source_bucket,
                    'backup': backup_bucket_name
                })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully created backups',
                'backups': backed_up_buckets
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error creating backups: {str(e)}'
            })
        }
