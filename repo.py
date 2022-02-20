import boto3
from boto3.dynamodb.conditions import Key
from constants import JOB_SITE_INDEED_ID

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('jobs')


def get_last_document():
    response = table.query(
        KeyConditionExpression=Key('site_id').eq(JOB_SITE_INDEED_ID),
        ScanIndexForward=False
    )

    items = response['Items']

    if len(items) > 0:
        return items[0]


def add_documents(items):
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
    print(f'[{len(items)} jobs added]')
