from models import Db


class BaseService:
    def __init__(self, db: Db):
        self.db = db


