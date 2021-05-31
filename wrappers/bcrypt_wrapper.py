import bcrypt


class BcryptWrapper:
    def gen_hash(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))

    def check(self, password: str, password_hash: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash)
