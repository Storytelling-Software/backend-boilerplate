import uuid
from pathlib import Path
from models import UploadedFile
from botocore.errorfactory import ClientError


class S3Wrapper:
    def __init__(self, s3_client, bucket_name, key_prefix) -> None:
        self.s3 = s3_client
        self.bucket_name = bucket_name
        self.key_prefix = key_prefix

    def upload_file(self, file, principal=None) -> UploadedFile or None:
        if not file:
            return None
        path = Path(file.filename)
        key = self.__generate_key(path.name)

        self.s3.upload_fileobj(file, self.bucket_name, key)
        return UploadedFile(key, path.name)

    def upload_io_file(self, io_file) -> None:
        if not io_file:
            return None
        key = self.__generate_io_key(io_file.name)
        self.s3.upload_fileobj(io_file, self.bucket_name, key)

    def list_objects(self) -> dict:
        try:
            return self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=self.key_prefix)
        except ClientError:
            return {}

    def delete_old_files(self, old_files) -> None:
        try:
            self.s3.delete_objects(Bucket=self.bucket_name, Delete={'Objects': old_files})
        except ClientError:
            pass

    def upload_path(self, path) -> UploadedFile or None:
        if not path:
            return None
        key = self.__generate_key(path.name)

        self.s3.upload_file(path, self.bucket_name, key)
        return UploadedFile(key, Path(path).name)

    def link(self, key) -> str or None:
        if not key:
            return None

        s3_request_params = {"Bucket": self.bucket_name, "Key": key}
        return self.s3.generate_presigned_url("get_object", Params=s3_request_params)

    def exists(self, key) -> bool or None:
        if not key:
            return None

        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            return False
        return True

    def delete(self, key) -> None:
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            pass

    def __generate_key(self, filename) -> str:
        return self.key_prefix + str(uuid.uuid4()) + "/" + filename

    def __generate_io_key(self, filename) -> str:
        return f'{self.key_prefix}{filename}'
