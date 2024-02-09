import sqlite3


class DbController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_db()

    def create_db(self):
        create_warn_count_table = '''
                            CREATE TABLE IF NOT EXISTS Warns (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                group_id INTEGER,
                                user_id INTEGER,
                                warn_count INTEGER
                            );
                        '''
        self.cursor.execute(create_warn_count_table)
        self.conn.commit()

    def create_warn_count_row(self, group_id, user_id):
        create_warn_count = '''
            INSERT INTO Warns (id, group_id, user_id, warn_count)
            VALUES (?, ?, ?, ?);
        '''
        self.cursor.execute(create_warn_count, (None, group_id, user_id, 0))
        self.conn.commit()

    def warn_user(self, group_id, user_id) -> int:
        update_warn_count = '''
            SELECT warn_count 
            FROM Warns 
            WHERE group_id = ? and user_id = ?;
        '''

        self.cursor.execute(update_warn_count, (group_id, user_id))
        warn_count = self.cursor.fetchone()[0] + 1

        if warn_count < 3:
            update_warn_count = '''
                                UPDATE Warns
                                SET warn_count = warn_count + 1
                                WHERE group_id = ? and user_id = ?;
                            '''
            self.cursor.execute(update_warn_count, (group_id, user_id))
        self.conn.commit()

        return warn_count

    def delete_warn_count(self, group_id, user_id):
        delete_warn_count = '''
            DELETE FROM Warns
            WHERE group_id = ? AND user_id = ?;
        '''

        self.cursor.execute(delete_warn_count, (group_id, user_id))
        self.conn.commit()