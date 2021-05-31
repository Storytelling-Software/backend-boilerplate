from models.uploaded_file import UploadedFile


class Profile:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.avatar = None

    @staticmethod
    def from_request(attributes: dict):
        profile = Profile()
        profile.first_name = attributes.get('first_name')
        profile.last_name = attributes.get('last_name')
        avatar_attributes = attributes.get('avatar')
        if avatar_attributes:
            profile.avatar = UploadedFile(
                avatar_attributes.get('key'), avatar_attributes.get('filename'))
        return profile

    def assign_request(self, attributes: dict) -> None:
        avatar_attributes = attributes.get('avatar')
        if avatar_attributes:
            self.avatar = UploadedFile(
                avatar_attributes.get('key'), avatar_attributes.get('filename'))
        self.first_name = attributes.get('first_name')
        self.last_name = attributes.get('last_name')

    def get_files(self):
        files = []
        if self.avatar:
            files.append(self.avatar)
        return files
