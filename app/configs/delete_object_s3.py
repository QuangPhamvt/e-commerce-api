import boto3


def delete_object_s3(bucket_name: str, object_name: str):
    """
    Delete object from S3 bucket

    :param bucket_name: str: S3 bucket name
    :param object_name: str: S3 object name
    :return: dict: response
    """

    s3_client = boto3.client("s3")
    response = s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    print(response)
    pass
