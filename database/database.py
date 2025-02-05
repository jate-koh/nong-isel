import sqlite3
import uuid

from utilities import get_logger


def get_database(path):
    return Database(path)


class Database:

    def __init__(self, path):
        self.logger = get_logger(module="Database")
        self.path = path
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()
        self.init_schema()

    def init_schema(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS UserGroup (id TEXT PRIMARY KEY, userId INTEGER, groupId TEXT)"
        )
        self.db.commit()
        self.logger.info("Database initialized.")

    def insert_usergroup(self, user_id, group_id):
        self.logger.debug(f"Inserting user {user_id} into group {group_id}")
        self.cursor.execute(
            "INSERT INTO UserGroup (id, userId, groupId) VALUES (?, ?, ?)",
            (f"{uuid.uuid4()}", user_id, group_id),
        )
        self.db.commit()

    def query(self, query, args=None):
        self.logger.debug(f"Executing query: {query}, args: {args}")
        try:
            self.cursor.execute(query, args)
            self.db.commit()
        except Exception as err:
            self.logger.error(f"Error executing query {query}", json_data=str(err))

    def close(self):
        self.db.close()
