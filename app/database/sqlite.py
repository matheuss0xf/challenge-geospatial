import sqlite3
from contextlib import contextmanager

from ..logger import logger
from .utils_sqlite import haversine


class DatabaseSqlite:
    def __init__(self, config):
        self.config = config

    def connect(self):
        conn = sqlite3.connect(self.config.DATABASE)
        conn.create_function('haversine', 4, haversine)
        conn.enable_load_extension(True)
        conn.execute("SELECT load_extension('mod_spatialite')")
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def get_cursor(self):
        conn = self.connect()
        try:
            yield conn, conn.cursor()
            conn.commit()
        except Exception as e:
            logger.exception('Database error occurred')
            conn.rollback()
            raise e
        finally:
            conn.close()
