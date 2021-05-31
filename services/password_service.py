class PasswordService:
    def __init__(self, bcrypt_wrapper, password_generator) -> None:
        self.bcrypt_wrapper = bcrypt_wrapper
        self.password_generator = password_generator

    def create_hash(self, password: str) -> bytes:
        return self.bcrypt_wrapper.gen_hash(password)

    def check(self, password, password_hash) -> bool:
        return self.bcrypt_wrapper.check(password, password_hash)

    def generate_password(self, length) -> str:
        return self.password_generator.generate_password(length)
