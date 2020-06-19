import os
import boto3

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_ACCESS_TOKEN = os.environ.get('AWS_ACCESS_TOKEN')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')


def aws_recognition(path):
    with open(path, 'rb') as file:
        image_bytes = bytearray(file.read())
    textract = boto3.client(service_name='textract', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_ACCESS_TOKEN, region_name=AWS_REGION_NAME)
    response = textract.detect_document_text(Document={'Bytes': image_bytes})
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            return item['Text'] or None
