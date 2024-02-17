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
                                chat_id INTEGER UNIQUE,
                                user_id INTEGER UNIQUE,
                                warn_count INTEGER
                            );
                        '''

        create_new_member_table = '''
                            CREATE TABLE IF NOT EXISTS NewMember (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                chat_id INTEGER UNIQUE,
                                user_id INTEGER UNIQUE,
                                answer INTEGER,
                                question_message_id INTEGER,
                                restriction_date DATE
                            );
                                '''

        self.cursor.execute(create_warn_count_table)
        self.cursor.execute(create_new_member_table)
        self.conn.commit()

    def create_warn_count_row(self, chat_id, user_id):
        create_warn_count_query = '''
            INSERT INTO Warns (id, chat_id, user_id, warn_count)
            VALUES (?, ?, ?, ?);
        '''
        self.cursor.execute(create_warn_count_query, (None, chat_id, user_id, 0))
        self.conn.commit()

    def create_new_member_row(self, chat_id, user_id, answer, question_message_id, restriction_date):
        create_new_member_row_query = '''
            INSERT INTO NewMember (id, chat_id, user_id, answer, question_message_id, restriction_date)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(create_new_member_row_query, (None,
                                                          chat_id,
                                                          user_id,
                                                          answer,
                                                          question_message_id,
                                                          restriction_date))
        self.conn.commit()

    def get_answer(self, chat_id, user_id):
        get_answer_query = '''
            SELECT answer FROM NewMember
            WHERE chat_id = ? and user_id = ?
        '''
        self.cursor.execute(get_answer_query, (chat_id, user_id))
        return self.cursor.fetchone()[0]

    def get_question_message_id(self, chat_id, user_id):
        get_answer_query = '''
            SELECT question_message_id FROM NewMember
            WHERE chat_id = ? and user_id = ?
        '''
        self.cursor.execute(get_answer_query, (chat_id, user_id))
        return self.cursor.fetchone()[0]

    def if_exists(self, chat_id, user_id):
        if_exists_query = '''
            SELECT user_id FROM NewMember
            WHERE chat_id = ? and user_id = ?
        '''

        self.cursor.execute(if_exists_query, (chat_id, user_id))
        return self.cursor.fetchone()[0]

    def delete_new_member(self, chat_id, user_id):
        delete_new_user_query = '''
            DELETE FROM NewMember
            WHERE chat_id = ? and user_id = ?
        '''

        self.cursor.execute(delete_new_user_query, (chat_id, user_id))
        self.conn.commit()

    def pop_non_responded_new_member_entities(self):
        select_non_responded_new_member_entities = '''
            SELECT user_id, chat_id FROM NewMember
            WHERE restriction_date < DATE('now');
        '''
        self.cursor.execute(select_non_responded_new_member_entities)
        result = self.cursor.fetchall()

        delete_non_responded_new_member_entities = '''
            DELETE FROM NewMember
            WHERE restriction_date < DATE('now');
        '''
        self.cursor.execute(delete_non_responded_new_member_entities)

        return result

    def warn_user(self, chat_id, user_id) -> int:
        update_warn_count = '''
            SELECT warn_count 
            FROM Warns 
            WHERE chat_id = ? and user_id = ?;
        '''

        self.cursor.execute(update_warn_count, (chat_id, user_id))
        warn_count = self.cursor.fetchone()[0] + 1

        if warn_count < 3:
            update_warn_count = '''
                                UPDATE Warns
                                SET warn_count = warn_count + 1
                                WHERE chat_id = ? and user_id = ?;
                            '''
            self.cursor.execute(update_warn_count, (chat_id, user_id))
        self.conn.commit()

        return warn_count

    def delete_warn_count_row(self, chat_id, user_id):
        delete_warn_count = '''
            DELETE FROM Warns
            WHERE chat_id = ? AND user_id = ?;
        '''

        self.cursor.execute(delete_warn_count, (chat_id, user_id))
        self.conn.commit()