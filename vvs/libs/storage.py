# Imports the Google Cloud client library
from google.cloud import storage
from google.api_core.exceptions import NotFound
import datetime

BASE_DIR = 'base'
DIFFERENCES_DIR = 'differences'
TARGETS_DIR = 'targets'
DEFAULT_BUCKET = 'validation-service'

class GoogleClient():

    def __init__(self):
        self.storage_client = storage.Client()

    def create_buckets(self, bucket_name):
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            print(f'Bucket { bucket.name } already exist. Ignoning creation')
        except NotFound as ex:
            bucket = self.storage_client.create_bucket(bucket_name)
            print(f'Bucket { bucket.name } created.')
    
    def upload_file(self, source_file_name, destination_blob_name):
        try:
            bucket = self.storage_client.bucket(DEFAULT_BUCKET)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            blob.make_public()
            
            print( f'File {source_file_name} uploaded to {destination_blob_name}.')

            return blob.public_url
            
        except Exception as ex:
            print(f'Something went wrong: {ex}')

if __name__ == "__main__":
    i = GoogleClient()
    i.create_buckets('vvs-test-buckets')