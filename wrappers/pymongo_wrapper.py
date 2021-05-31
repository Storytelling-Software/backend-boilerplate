import pymongo


class PymongoWrapper:
    def __init__(self, environment_wrapper) -> None:
        self.scheme = environment_wrapper.get_var('MONGO_SCHEME')
        self.username = environment_wrapper.get_var('MONGO_USERNAME')
        self.password = environment_wrapper.get_var('MONGO_PASSWORD')
        self.host = environment_wrapper.get_var('MONGO_HOST')
        self.port = environment_wrapper.get_var('MONGO_PORT')
        self.name = environment_wrapper.get_var('MONGO_NAME')

    def get_client(self):
        credentials = ''
        if self.username:
            credentials = f'{self.username}:{self.password}@'
        url = f'{self.scheme}://{credentials}{self.host}:{self.port}'
        return pymongo.MongoClient(url)

    def get_collection(self, client, collection_name: str):
        return client[self.name][collection_name]
