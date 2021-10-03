import sqlite3


class DataBase:
    def __init__(self, path: str):
        self.path = path

    def __connection(self):
        return sqlite3.connect(self.path)

    def __execute(self, sql: str, fetchone=False, fetchall=False, commit=False):
        conn = self.__connection()
        cursor = conn.cursor()
        data = None
        cursor.execute(sql)

        if commit:
            conn.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        conn.close()
        return data

    def add_user(self, telegram_id: int, name: str, age: int, gender: str, roommate_gender: str,
                 smoking: int, number_of_rooms: int, about: str, photo_id: str):
        sql = f"""
        INSERT INTO questionnaires
        VALUES ({telegram_id}, '{name}', {age}, '{gender}', '{roommate_gender}', {smoking}, {number_of_rooms}, '{about}', '{photo_id}')
        """
        self.__execute(sql, commit=True)

    def questionnaire_in_table(self, telegram_id: int) -> bool:
        sql = f"""
        SELECT EXISTS(SELECT telegram_id FROM questionnaires
        WHERE telegram_id = {telegram_id})
        """
        if self.__execute(sql, fetchone=True)[0] == 0:
            return False
        else:
            return True

    def get_questionnaire(self, telegram_id: int):
        sql = f"""
        SELECT * FROM questionnaires
        WHERE telegram_id = {telegram_id}
        """
        return self.__execute(sql, fetchone=True)

    def delete_questionnaire(self, telegram_id: int):
        sql = f"""
            DELETE FROM questionnaires
            WHERE telegram_id = {telegram_id};
        """
        self.__execute(sql, commit=True)

    def change_field(self, field_name: str, field_value: str, telegram_id: int):
        sql = f"""
        UPDATE questionnaires
        SET {field_name} = {field_value}
        WHERE telegram_id = {telegram_id}
        """
        self.__execute(sql, commit=True)