import os
import json

from todos import decimalencoder
import boto3

traducir = boto3.client('translate')
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    task_text = result['Item']['text']
    idioma_dest = event['pathParameters']['lang']
    try: 
        result_trans = traducir.translate_text(
		    Text=task_text,
		    SourceLanguageCode="auto", 
		    TargetLanguageCode=idioma_dest
	    )
    except Exception as e:
        raise Exception("[ErrorMessage]: " + str(e))
	
	
    result['Item']["text"]=str(result_trans["TranslatedText"])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response