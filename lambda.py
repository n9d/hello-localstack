
import json
def lambda_handler(event, context):
    print("hello world")

    return {
        'statusCode': 200,
        'body': {
            'message': f'Hello world!!',
        }
    }


