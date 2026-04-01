import json
import boto3

sqs = boto3.client('sqs')

QUEUE_URL = "YOUR_SQS_QUEUE_URL"

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])

        retry_count = body.get("retryCount", 0)

        print("========== NEW EXECUTION ==========")
        print("Received:", body)

        success = process_payment(body)

        if not success:
            retry_count += 1

            if retry_count < 3:
                body["retryCount"] = retry_count

                print(f"Retrying... attempt {retry_count}")

                sqs.send_message(
                    QueueUrl=QUEUE_URL,
                    MessageBody=json.dumps(body),
                    DelaySeconds=10
                )
            else:
                print("Max retries reached → DLQ")

def process_payment(data):
    return False
