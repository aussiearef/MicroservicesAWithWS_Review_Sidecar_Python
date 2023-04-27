import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Booking')

def lambda_handler(event, context):
    for record in event['Records']:
        sns_message = json.loads(record['Sns']['Message'])
        booking_id = sns_message.get('BookingId')
        status = sns_message.get('Status')
        if not booking_id:
            print('SNS Event did not return a valid BookingId')
            continue
        try:
            response = table.update_item(
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
            print(f'Booking with ID {booking_id} updated successfully.')
        except Exception as e:
            print(f'Error updating booking with ID {booking_id}: {e}')
