import boto3
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    try:
        # List all S3 buckets
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in
                    response['Buckets']]

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Successfully discovered buckets',
                'resources': buckets
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': f'Error discovering buckets: {str(e)}'
            })
        }