from models import Profile


class ProfileMongoTranslator:
    def __init__(self, uploaded_file_translator):
        self.uploaded_file_translator = uploaded_file_translator

    def to_document(self, profile) -> dict:
        return {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'avatar': self.uploaded_file_translator.to_document(profile.avatar),
        }

    def from_document(self, document) -> Profile:
        profile = Profile()
        profile.first_name = document.get('first_name')
        profile.last_name = document.get('last_name')
        profile.avatar = self.uploaded_file_translator.from_document(
            document.get('avatar', {}))
        return profile
