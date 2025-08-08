import boto3
from django.conf import settings
from datetime import datetime

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_DEFAULT_REGION
)

def upload_file(file, file_name) -> str:
    timeStamp = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_key = f'facturas/{file_name}_{timeStamp}'
    try:
        s3.upload_fileobj(
            file,
            settings.BUCKET_NAME,
            s3_key,
            ExtraArgs={'ACL': 'public-read'}
        )
        return f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
    except Exception as e:
        raise e