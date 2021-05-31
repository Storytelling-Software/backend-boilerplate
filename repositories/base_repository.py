from bson import ObjectId


class BaseRepository:
    def __init__(self, collection, model_translator, default_scope, indexes):
        self.indexes = indexes
        self.default_scope = default_scope
        self.collection = collection
        self.model_translator = model_translator
        self.__configure_indexes()

    def create(self, model) -> str:
        document = self.model_translator.to_document(model)
        document.pop('_id')
        return self.collection.insert_one(document).inserted_id

    def update(self, model) -> None:
        document = self.model_translator.to_document(model)
        self.collection.update_one(
            {'_id': ObjectId(model.id)}, {'$set': document})

    def delete(self, model) -> None:
        self.collection.delete_one({'_id': ObjectId(model.id)})

    def delete_all(self) -> None:
        self.collection.delete_many({})

    def find_by_id(self, model_id):
        object_id = self._parse_object_id(model_id)
        pipeline = [
            {'$match': {'_id': object_id}}
        ]
        return self._find_one_by_aggregation(pipeline + self.default_scope)

    def find_by_ids_list(self, ids_list) -> list:
        ids = [self._parse_object_id(arg_id) for arg_id in ids_list]
        pipeline = [{'$match': {'_id': {'$in': ids}}}]
        return self._find_by_aggregation(pipeline + self.default_scope)

    def get_page(self, skip, limit) -> list:
        return self._find_by_aggregation(self.default_scope + [
            {'$skip': skip},
            {'$limit': limit}
        ])

    def get_list(self) -> list:
        pipeline = [
            {
                "$match": {}
            }
        ]
        return self._find_by_aggregation(pipeline + self.default_scope)

    def _find_by_aggregation(self, pipeline) -> list:
        cursor = self.collection.aggregate(pipeline)
        result = [self.model_translator.from_document(d) for d in cursor]
        return result

    def _find_one_by_aggregation(self, pipeline):
        result = self._find_by_aggregation(pipeline)
        if not result:
            return None
        return result[0]

    def _count_by_aggregation(self, pipeline) -> int:
        group_step = {'$group': {'_id': None, 'count': {'$sum': 1}}}
        project_step = {'$project': {'_id': 0}}

        cursor = self.collection.aggregate(pipeline + [group_step, project_step])
        result = [item.get('count') for item in cursor]
        if not result:
            return 0
        return result[0]

    def _parse_object_id(self, model_id) -> ObjectId or None:
        if isinstance(model_id, ObjectId):
            return model_id
        if ObjectId.is_valid(model_id):
            return ObjectId(model_id)
        return None

    def __configure_indexes(self) -> None:
        if type(self.indexes) != list:
            return None
        existing_indexes = self.collection.index_information()
        new_indexes = [
            index for index in self.indexes if index not in existing_indexes.keys()
        ]
        if new_indexes:
            self.collection.create_indexes(new_indexes)
