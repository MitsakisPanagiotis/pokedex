from algoliasearch.search.client import SearchClientSync


class Algolia:
    def __init__(self, app_id, write_api_key):
        self.client = SearchClientSync(app_id, write_api_key)

    def save(self, obj):
        return self.client.save_object(index_name="pokemon", body=obj)
