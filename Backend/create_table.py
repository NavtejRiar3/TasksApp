import boto3
import json
from botocore.exceptions import ClientError

def load_schema(schema_file):
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    return schema

def create_dynamodb_table(schema_file):
    # Load the schema from the file
    schema = load_schema(schema_file)

    # Set up the DynamoDB client
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url="http://localhost:8000",  # Use this if running DynamoDB locally
        region_name="us-west-2",               # Change to your preferred region if using AWS
        aws_access_key_id="fakeMyKeyId",       # Not needed for local use, but required fields
        aws_secret_access_key="fakeSecretAccessKey"
    )

    # Create the table using the loaded schema
    try:
        table = dynamodb.create_table(**schema)

        # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName=schema['TableName'])
        print("Table status:", table.table_status)

    except ClientError as e:
        print(f"Error creating table: {e.response['Error']['Message']}")

if __name__ == '__main__':
    create_dynamodb_table('db_schema.json')
