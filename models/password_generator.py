import random


class PasswordPartGenerator:
    def __init__(self, characters):
        self.characters = characters

    def generate(self, length):
        random_characters = random.choices(self.characters, k=length)
        return random_characters


class PasswordGenerator:
    def __init__(self, generators: list):
        self.generators = generators

    def generate_password(self, length):
        sliced_generated_parts = []
        generated_parts = len(self.generators)
        for generator in self.generators[:-1]:
            sliced_length = random.randint(1, length - generated_parts + 1)
            generated_parts -= 1
            length -= sliced_length
            sliced_generated_parts.append(generator.generate(sliced_length))
        sliced_generated_parts.append(self.generators[-1].generate(length))

        password_characters = [item for sublist in sliced_generated_parts for item in sublist]
        random.shuffle(password_characters)
        generated_password = ''.join(password_characters)
        return generated_password
