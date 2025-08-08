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
    try:
        s3.upload_fileobj(
            file,
            settings.BUCKET_NAME,
            f"{timeStamp}_{file_name}",
            ExtraArgs={'ACL': 'public-read'}
        )
        return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{timeStamp}_{file_name}"
    except Exception as e:
        raise e