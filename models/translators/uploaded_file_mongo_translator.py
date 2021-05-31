from models import UploadedFile


class UploadedFileMongoTranslator:
    def to_document(self, uploaded_file):
        if not uploaded_file:
            return None
        return {
            'key': uploaded_file.key,
            'filename': uploaded_file.filename
        }
    
    def from_document(self, document):
        if not document:
            return None
        return UploadedFile(document.get('key'), document.get('filename'))
