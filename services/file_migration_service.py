from infrastructure.exceptions import InvalidRequestException


class FileMigrationService:
    def __init__(self, s3_resource, main_s3_wrapper, temp_s3_wrapper) -> None:
        self.s3_resource = s3_resource
        self.main_s3_wrapper = main_s3_wrapper
        self.temp_s3_wrapper = temp_s3_wrapper

    def migrate(self, files) -> None:
        missing_keys = []
        for file in files:
            if self.main_s3_wrapper.exists(file.key):
                continue

            if not self.temp_s3_wrapper.exists(file.key):
                missing_keys.append(file.key)
                continue

            bucket = self.s3_resource.Bucket(self.main_s3_wrapper.bucket_name)
            bucket.copy({
                'Bucket': self.temp_s3_wrapper.bucket_name,
                'Key': file.key
            }, file.key)
            self.temp_s3_wrapper.delete(file.key)

        if missing_keys:
            raise InvalidRequestException({'missing_keys': missing_keys})
