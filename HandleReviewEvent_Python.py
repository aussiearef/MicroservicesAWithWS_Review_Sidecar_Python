import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Booking')

def lambda_handler(event, context):
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    booking_id = sns_message.get('BookingId')
    status = sns_message.get('Status')
    table.update_item(
        Key={
            'Id': booking_id
        },
        UpdateExpression='SET #status = :val',
        ExpressionAttributeNames={
            '#status': 'Status'
        },
        ExpressionAttributeValues={
            ':val': status
        }
    )
    context.log(f"Booking with ID {booking_id} updated successfully.")
        
