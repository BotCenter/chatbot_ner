import errno
import os

import boto3


def assert_dir_exists(path):
    """
    Checks if directory tree in path exists. If not it created them.
    :param path: the path to check if it exists
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def download_dir(client, bucket, path, target):
    """
    Downloads recursively the given S3 path to the target directory.
    :param client: S3 client to use.
    :param bucket: the name of the bucket to download from
    :param path: The S3 directory to download.
    :param target: the local directory to download the files to.
    """

    # Handle missing / at end of prefix
    if not path.endswith('/'):
        path += '/'

    paginator = client.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket, Prefix=path):
        # Download each file individually
        for key in result['Contents']:
            # Calculate relative path
            rel_path = key['Key'][len(path):]
            # Skip paths ending in /
            if not key['Key'].endswith('/'):
                local_file_path = os.path.join(target, rel_path)
                # Make sure directories exist
                local_file_dir = os.path.dirname(local_file_path)
                assert_dir_exists(local_file_dir)
                print("Downloading data of " + str(key['Key']))
                client.download_file(bucket, key['Key'], local_file_path)



def execute_download():
    '''
    This function downloads all entities CSV data from a bucket in S3 to
    load as entities in elasticsearch and chatbot-ner
    :return:
    '''
    s3 = boto3.client('s3')
    print("Downloading S3 Data")
    download_dir(s3, 'botcenter-chatbot-ner', 'entity_data', 'data/entity_data')
    print("Download S3 Data Done!")


execute_download()
