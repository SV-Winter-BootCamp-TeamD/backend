from threading import Lock
import boto3, os

lock = Lock()

def upload_file_to_s3(img_file, key, ExtraArgs):
    with lock:
        s3 = boto3.client(
            "s3",
            aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY')
        )

    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    try:
        s3.upload_fileobj(img_file, bucket_name, key, ExtraArgs)
        img_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        return img_url
    except Exception as e:
        print(f"error: {e}")
        return None