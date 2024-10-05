from pymongo import MongoClient

class Connection:
    # Singleton pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri: str, db: str):
        if not hasattr(self, '_is_init'):
            self._is_init = True
            self._uri = uri
            self.db_name = db
            self._client = None
            self._db = None
            self._connect()

    def _connect(self):
        try:
            self._client = MongoClient(self._uri)
            self._db = self._client[self.db_name]
        except Exception as e:
            self._client = None
            self._db = None

    @property
    def db(self):
        return self._db
