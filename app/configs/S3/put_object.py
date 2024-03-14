import logging
import boto3
from botocore.exceptions import ClientError

from app.configs.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def put_object(bucket_name, object_name, expiration=3600) -> str | None:
    """
    Generate a presigned URL to share an S3 object
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    response = None
    try:
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
                "ContentType": "image/png",
            },
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
