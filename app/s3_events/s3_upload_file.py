import os
from fastapi import HTTPException
import datetime
from functools import lru_cache

from config import Settings
from s3_events.s3_utils import S3SERVICE


@lru_cache()
def get_settings():
    return Settings()


AWS_ACCESS_KEY_ID = get_settings().AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = get_settings().AWS_SECRET_ACCESS_KEY
AWS_REGION = get_settings().AWS_REGION
S3_Bucket = get_settings().S3_Bucket
S3_Key = get_settings().S3_Key

s3_client = S3SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)


def upload_to_s3(fileobject):
    filename = fileobject.filename
    current_time = datetime.datetime.now()
    split_file_name = os.path.splitext(filename)
    file_name_unique = str(current_time.timestamp()).replace('.', '')
    file_extension = split_file_name[1]
    data = fileobject.file
    uploads3 = s3_client.upload_fileobj(bucket=S3_Bucket,
                                        key=S3_Key + file_name_unique + file_extension,
                                        file_name=data)
    if uploads3:
        s3_url = f"https://{S3_Bucket}.s3.{AWS_REGION}.amazonaws.com/{S3_Key}{file_name_unique +  file_extension}"
        #return {"status": "success", "image_url": s3_url}
        return s3_url
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")