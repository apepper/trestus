# for logging
import logging
# for decryption and s3 handling
import boto3
from os import environ, path
from base64 import b64decode
# for trestus
import trestus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# local development
# API_KEY = environ['API_KEY']
# TOKEN = environ['TOKEN']

ENCRYPTED_API_KEY = environ['API_KEY']
API_KEY = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_API_KEY))['Plaintext']
ENCRYPTED_TOKEN = environ['TOKEN']
TOKEN = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_TOKEN))['Plaintext']
BOARD_ID = environ['BOARD_ID']
BUCKET_NAME = environ['BUCKET_NAME']
CUSTOM_TEMPLATE = environ['CUSTOM_TEMPLATE']
OUTPUT_PATH= environ['OUTPUT_PATH']

def s3_upload(source_path):
    import mimetypes
    s3 = boto3.resource('s3')
    s3.Object(BUCKET_NAME, path.basename(source_path)).upload_file(source_path,{'ContentType':mimetypes.guess_type(source_path)[0]})

def calltrestus_handler(event, context):
    import sys
    logger.info('Received event: {}'.format(event))
    sys.argv += ['--board-id', BOARD_ID, '--key', API_KEY, '--token', TOKEN,'--custom-template', CUSTOM_TEMPLATE, OUTPUT_PATH]
    trestus.main()
    css_path = path.join(path.dirname(OUTPUT_PATH), 'trestus.css')
    for path_to_upload in [OUTPUT_PATH, css_path, './robots.txt']:
        logger.info('Upload file to S3: {}'.format(path_to_upload))
        s3_upload(path_to_upload)

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    print calltrestus_handler("event", "context")
