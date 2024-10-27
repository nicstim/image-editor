import json

from minio import Minio

from app.config import settings

PUBLIC_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET_NAME}/*"]
        }
    ]
}

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)
if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
    minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
minio_client.set_bucket_policy(
    settings.MINIO_BUCKET_NAME,
    json.dumps(PUBLIC_POLICY)
)
