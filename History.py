import sqlite3
from datetime import datetime


class History:

    def __init__(self, path_to_db_file):
        self.conn = sqlite3.connect(path_to_db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS file_info
                            (id INTEGER PRIMARY KEY,
                            path TEXT,
                            date_of_use TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS triangle_parameters
                            (file_id INTEGER NOT NULL REFERENCES file_info(id), 
                            min_height INTEGER, max_height INTEGER,
                            step_x INTEGER, step_y INTEGER,
                            max_discrepancy INTEGER)""")
        self.conn.commit()

    def load(self):
        self.cursor.execute("SELECT * FROM file_info ORDER BY id DESC")
        return self.cursor.fetchall()

    def update(self,
               map_filename,
               min_height, max_height,
               step_x, step_y,
               max_discrepancy):
        self.cursor.execute("SELECT COUNT(id) FROM file_info")
        row_count = self.cursor.fetchone()[0]
        self.cursor.execute(f"""INSERT INTO file_info VALUES (?,?,?);""",
                            (row_count + 1,
                             map_filename,
                             datetime.today().strftime('%d.%m.%Y %H:%M')))
        self.cursor.execute(f"""INSERT INTO triangle_parameters VALUES (?,?,?,?,?,?);""",
                            (row_count + 1,
                             min_height, max_height,
                             step_x, step_y,
                             max_discrepancy))
        self.conn.commit()
        if row_count == 5:
            self.cursor.execute(f"""DELETE FROM triangle_parameters WHERE file_id = ?""", (1,))
            self.cursor.execute(f"""DELETE FROM file_info WHERE id = ?""", (1,))
            self.cursor.execute(f"""UPDATE triangle_parameters SET file_id = file_id-1""")
            self.cursor.execute(f"""UPDATE file_info SET id = id-1""")
            self.conn.commit()

    def select_row_file_info(self, id_row):
        self.cursor.execute("SELECT * FROM file_info WHERE id=?", (id_row,))
        return self.cursor.fetchone()

    def select_row_triangle_parameters(self, id_row):
        self.cursor.execute("SELECT * FROM triangle_parameters WHERE file_id=?", (id_row,))
        return self.cursor.fetchone()
