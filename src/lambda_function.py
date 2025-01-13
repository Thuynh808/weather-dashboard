import os
import json
import boto3

# Initialize AWS clients
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Environment variables
sns_topic_arn = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    try:
        # Extract bucket name and object key from the EventBridge event
        bucket = event['detail']['bucket']['name']
        key = event['detail']['object']['key']

        # Retrieve the aggregated weather data
        response = s3_client.get_object(Bucket=bucket, Key=key)
        aggregated_data = json.loads(response['Body'].read().decode('utf-8'))

        # Format the aggregated weather report
        message = "Weather Dashboard Report:\n\n"
        for city, data in aggregated_data.items():
            message += (
                f"City: {city}\n"
                f"- Temperature: {data.get('temperature', 'N/A')}\n"
                f"- Feels Like: {data.get('feels_like', 'N/A')}\n"
                f"- Humidity: {data.get('humidity', 'N/A')}\n"
                f"- Conditions: {data.get('conditions', 'N/A')}\n"
                f"- Wind Speed: {data.get('wind_speed', 'N/A')}\n"
                f"- Sunrise: {data.get('sunrise', 'N/A')}\n"
                f"- Sunset: {data.get('sunset', 'N/A')}\n\n"
            )

        # Publish the aggregated report to SNS
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="Weather Dashboard Report",
            Message=message
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Weather report sent successfully.')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing weather data: {str(e)}")
        }

