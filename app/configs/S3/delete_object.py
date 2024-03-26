import boto3
import logging

from app.configs.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def delete_object_s3(bucket_name: str, object_name: str):
    """
    Delete object from S3 bucket

    :param bucket_name: str: S3 bucket name
    :param object_name: str: S3 object name
    :return: dict: response
    """

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = None
    try:
        response = s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    except Exception as e:
        logging.error(e)
        return None

    return response
