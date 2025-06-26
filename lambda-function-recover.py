import boto3
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    try:
        # List all buckets
        response = s3_client.list_buckets()
        all_buckets = [bucket['Name'] for bucket in response['Buckets']]
        
        # Find backup buckets
        backup_buckets = [b for b in all_buckets if '-backup-' in b]
        recovered = []
        
        for backup_bucket in backup_buckets:
            # Get original bucket name
            original_bucket = backup_bucket.split('-backup-')[0]
            
            # Create original bucket if it doesn't exist
            if original_bucket not in all_buckets:
                s3_client.create_bucket(Bucket=original_bucket)
            
            # Copy objects back
            paginator = s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=backup_bucket):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        copy_source = {
                            'Bucket': backup_bucket,
                            'Key': obj['Key']
                        }
                        s3_client.copy_object(
                            CopySource=copy_source,
                            Bucket=original_bucket,
                            Key=obj['Key']
                        )
            
            recovered.append({
                'backup': backup_bucket,
                'recovered_to': original_bucket
            })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully recovered buckets',
                'recovered': recovered
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error recovering buckets: {str(e)}'
            })
        }