import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def database_init(self, db, log_warn):
        db.create_table('users', 
                        id='INTEGER', 
                        username='TEXT',
                        first_name='TEXT',
                        last_name='TEXT',
                        custom_nickname='TEXT',
                        language_code='TEXT',
                        age='INTEGER',
                        city='TEXT',
                        personality ='TEXT',
                        gender ='TEXT',
                        zodiac='TEXT', 
                        birthdate='DATETIME',
                        when_added='DATETIME',
                        coins='INTEGER',
                        amethysts='INTEGER',
                        vip='BOOL',
                        relationship='JSON',
                        characters='JSON',
                        rp='JSON',
                        dick='INTEGER',
                        tea='INTEGER',
                        beer='INTEGER',
                        coffee='INTEGER',
                        kymyz='INTEGER',
                        energy='INTEGER',
                        timers='JSON',
                        )
        db.create_table('groups', 
                        id='INTEGER', 
                        title='TEXT', 
                        dscription='TEXT', 
                        invite_link='TEXT', 
                        status="TEXT",
                        members='JSON',
                        dk='JSON',
                        day_stat='JSON',
                        week_stat='JSON',
                        month_stat='JSON',
                        year_stat='JSON',
                        all_stat='JSON',
                        active='JSON',
                        inactive='JSON',
                        pairings='JSON',
                        anons='BOOL',
                        admin_chat='BOOL',
                        debug='BOOL',
                        config='BOOL',
                        )
        db.create_table('intel', 
                        id='INTEGER PRIMARY KEY', 
                        input_text='TEXT',
                        input_id='INTEGER',
                        output_text='TEXT',
                        output_id='INTEGER',
                        )
        log_warn("DATABASE INITIALIZED")
        
    def create_table(self, table_name, **columns):
        # Создание таблицы, если она не существует
        columns_definition = ', '.join(f'{col} {col_type}' for col, col_type in columns.items())
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});'
        self.cursor.execute(create_table_query)
        self.conn.commit()
        
        # Получение текущих столбцов таблицы
        self.cursor.execute(f'PRAGMA table_info({table_name});')
        existing_columns = {row[1]: row[2] for row in self.cursor.fetchall()}
        
        # Определение столбцов, которые нужно удалить и добавить
        new_columns = {col: col_type for col, col_type in columns.items() if col not in existing_columns}
        columns_to_remove = [col for col in existing_columns if col not in columns]
        
        # Если нужно удалить столбцы
        if columns_to_remove:
            # Создание временной таблицы с новой структурой
            temp_table_name = f'{table_name}_temp'
            temp_columns_definition = ', '.join(f'{col} {col_type}' for col, col_type in {**columns, **existing_columns}.items())
            create_temp_table_query = f'CREATE TABLE {temp_table_name} ({temp_columns_definition});'
            self.cursor.execute(create_temp_table_query)
            
            # Копирование данных из оригинальной таблицы во временную таблицу
            existing_columns_str = ', '.join(existing_columns.keys())
            copy_data_query = f'INSERT INTO {temp_table_name} ({existing_columns_str}) SELECT {existing_columns_str} FROM {table_name};'
            self.cursor.execute(copy_data_query)
            
            # Удаление оригинальной таблицы
            drop_table_query = f'DROP TABLE {table_name};'
            self.cursor.execute(drop_table_query)
            
            # Переименование временной таблицы в оригинальную
            rename_table_query = f'ALTER TABLE {temp_table_name} RENAME TO {table_name};'
            self.cursor.execute(rename_table_query)
            
            self.conn.commit()



    def insert_data(self, table_name, **data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders});'
        self.cursor.execute(insert_query, tuple(data.values()))
        self.conn.commit()

    def update_data(self, table_name, where_clause, where_args, **data):
        set_clause = ', '.join(f'{col} = ?' for col in data)
        update_query = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause};'
        self.cursor.execute(update_query, (*data.values(), *where_args))
        self.conn.commit()
    
    def update_data_from_dict(self, table_name, where_clause, where_args, data):
        set_clause = ', '.join(f'{col} = ?' for col in data)
        update_query = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause};'
        self.cursor.execute(update_query, (*data.values(), *where_args))
        self.conn.commit()

    def fetch_data(self, table_name, where_clause=None, where_args=()):
        # Fetch the column names
        self.cursor.execute(f'PRAGMA table_info({table_name});')
        columns = [column[1] for column in self.cursor.fetchall()]

        # Fetch the data
        if where_clause:
            fetch_query = f'SELECT * FROM {table_name} WHERE {where_clause};'
            self.cursor.execute(fetch_query, where_args)
        else:
            fetch_query = f'SELECT * FROM {table_name};'
            self.cursor.execute(fetch_query)

        rows = self.cursor.fetchall()
        
        # Create a list of dictionaries
        result = [dict(zip(columns, row)) for row in rows]
        
        return result


    def find_by_column(self, table_name, column, value):
        query = f'SELECT * FROM {table_name} WHERE {column} = ?;'
        self.cursor.execute(query, (value,))
        rows = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]
        return result

    def exists(self, table_name, column, value):
        query = f'SELECT 1 FROM {table_name} WHERE {column} = ? LIMIT 1;'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchone() is not None

    def check_user_value(self, table_name, user_column, user_value, check_column):
        query = f'SELECT {check_column} FROM {table_name} WHERE {user_column} = ?;'
        self.cursor.execute(query, (user_value,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def delete_data(self, table_name, where_clause, where_args):
        """
        Удаляет строки из таблицы на основе условия.
        
        :param table_name: Имя таблицы
        :param where_clause: Условие для удаления строк (например, "id = ?")
        :param where_args: Значения для условия (например, (1,))
        """
        delete_query = f'DELETE FROM {table_name} WHERE {where_clause};'
        self.cursor.execute(delete_query, where_args)
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    conn = sqlite3.connect('aicy.db')
    cursor = conn.cursor()
    drop_table_query = input('cmd $ >')
    cursor.execute(drop_table_query)
    quit()


#  # Пример использования
#  db = DatabaseManager('example.db')

#  # Создание таблицы
#  db.create_table('users', id='INTEGER PRIMARY KEY', name='TEXT', age='INTEGER')

#  # Вставка данных
#  db.insert_data('users', name='John Doe', age=30)

#  # Обновление данных
#  db.update_data('users', 'id = ?', (1,), name='Jane Doe', age=25)

#  # Извлечение данных
#  users = db.fetch_data('users')
#  print(users)

#  # Нахождение пользователя по имени
#  user = db.find_by_column('users', 'name', 'Jane Doe')
#  print(user)

#  # Проверка на наличие пользователя в БД
#  exists = db.exists('users', 'name', 'Jane Doe')
#  print(f'User exists: {exists}')

#  # Проверка значения возраста у пользователя
#  age = db.check_user_value('users', 'name', 'Jane Doe', 'age')
#  print(f'Jane Doe\'s age: {age}')

#  # Закрытие соединения
#  db.close()