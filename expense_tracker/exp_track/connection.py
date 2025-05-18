from PySide6 import QtWidgets, QtSql


from PySide6 import QtWidgets, QtSql

# Реализация базы данных.
class Data:
    def __init__(self):
        super(Data, self).__init__()
        # Предназначин для подключений к базе данных. И создания тадлицы если нет.
        self.create_connection()  # Вызываем автоматически что он создавл БД.

    def create_connection(self):
        # Используемый дравер базы данных QtSql
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        # Устанавливаем Имя БД
        db.setDatabaseName('expense_db.db')
        # Проверка Удалось ли открыть БД и выведем сообщение в диалоговое окно.
        # Open + Обект db
        if not db.open():
            QtWidgets.QMessageBox.critical(None, "Cannot open database",
                                           "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
            return False # Нам не удалсь.

        query = QtSql.QSqlQuery()
        # Передаем запрос.
        # Определение полей ID / Date / Category / Description / Balance / Status
        query.exec("CREATE TABLE IF NOT EXISTS expenses "
                   "(ID integer primary key AUTOINCREMENT, Date VARCHAR(20), "
                   "Category VARCHAR(20), Description VARCHAR(20), Balance REAL, Status VARCHAR(20))")
        return True


    # Метод добавления. Удаления. Запрос.
    # Строку sql_query -запроса и query_values=None -значение.
    def execute_query_with_params(self, sql_query, query_values=None):

        query = QtSql.QSqlQuery()  # Создаем Объект запросо
        # Подгатовка запроса. Создает строку запроса. Передаеться текст в Формате SQL
        query.prepare(sql_query) # Обединяет параметр исам запрос.

        # Оформить запрос в качесте параметра.
        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()  # Выполняем запрос. Вернет Trye or False

        return query

    # Добавление Транзакци. Создает SQL Запрос.
    def add_new_transaction_query(self, date, category, description, balance, status):
        # Новая строка. INSERT INTO -Новая запись
        sql_query = "INSERT INTO expenses (Date, Category, Description, Balance, Status) VALUES (?, ?, ?, ?, ?)"
        # Предаем переменную.  список значени полей для добавления.
        self.execute_query_with_params(sql_query, [date, category, description, balance, status])

    # Метод редактирования.
    def update_transaction_query(self, date, category, description, balance, status, id):
        # Формируем Запрос. UPDATE однавление записи. SET Date=? -Наименование полей к изминению. WHERE ID=? -Указать где изменить.
        sql_query = "UPDATE expenses SET Date=?, Category=?, Description=?, Balance=?, Status=? WHERE ID=?"
        self.execute_query_with_params(sql_query, [date, category, description, balance, status, id])

    # Удаление только 1 Аргумент. ID
    def delete_transaction_query(self, id):
        # Сохраняем запрос.
        sql_query = "DELETE FROM expenses WHERE ID=?"
        # Вызываем и передаем Список аргумета.
        self.execute_query_with_params(sql_query, [id])


    # Предоставление данных сум по категории. Расхода и дохода.
    # Для расчета сумм выполняем запросы к БД Получение значени по полям.
    # Общая ФУНК обин и тот запрос. С разными Фильтрами наименование полей и содержимом.
    # Просто вычесляет занчение в столбце. Фильтрует запросы с параметрами.
    # filter -фильтруем поле. value -значени содержиться в отфильтрованом значение.
    def get_total(self, column, filter=None, value=None):
        # Опредиляем строку с запросом. SELECT SUM -Наименование полей.
        sql_query = f"SELECT SUM({column}) FROM expenses"

        # Проверка. передано ли данному методу.
        if filter is not None and value is not None:
            # {filter} -Подставит значение к запросу
            sql_query += f" WHERE {filter} = ?"

        # Список значений для постановки запросов.
        query_values = []

        if value is not None:
            # Добавляем значение.
            query_values.append(value)

        # Поместить в переменную
        query = self.execute_query_with_params(sql_query, query_values)

        # Результат запроса. $ -Пибавляем знак.
        # next() -Для получение следующего.
        if query.next():
            # value -Сумма столбца. Конвертируем в строку и добавляет $
            return str(query.value(0)) + '$'

        return '0'

    # Методы побсчета.
    def total_balance(self):
        # Сумируем всю таблицу по балансу.
        return self.get_total(column="Balance")

    def total_income(self):
        # Фильтруем по Income.
        return self.get_total(column="Balance", filter="Status", value="Income")

    def total_outcome(self):
        # Фильтруем по расходу.
        return self.get_total(column="Balance", filter="Status", value="Outcome")

    def total_groceries(self):
        return self.get_total(column="Balance", filter="Category", value="Grocery")

    def total_auto(self):

        return self.get_total(column="Balance", filter="Category", value="Auto")

    def total_entertainment(self):
        return self.get_total(column="Balance", filter="Category", value="Entertainment")

    def total_other(self):
        return self.get_total(column="Balance", filter="Category", value="Other")

        
        
# class Data:
#     def __init__(self):
#         super(Data, self).__init__()
#         self.create_connection() # Инициализация подключения

#     def create_connection(self):
#         """SQLite: Используется встроенная БД. Автоматическое создание таблицы при первом запуске."""
#         db = QtSql.QSqlDatabase.addDatabase('QSQLITE') # Драйвер SQLite
#         db.setDatabaseName('.\expense_db.db')

#         if not db.open():
#             # Обработка ошибки подключения
#             QtWidgets.QMessageBox.critical(None, "Cannot open database",
#                                            "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
#             return False

#         # Создание таблицы, если не существует
#         query = QtSql.QSqlQuery()
#         query.exec("CREATE TABLE IF NOT EXISTS expenses (ID integer primary key AUTOINCREMENT, Date VARCHAR(20), "
#                    "Category VARCHAR(20), Description VARCHAR(20), Balance REAL, Status VARCHAR(20))")
#         return True

#     def execute_query_with_params(self, sql_query, query_values=None):
#         query = QtSql.QSqlQuery()
#         query.prepare(sql_query)

#         if query_values is not None:
#             for query_value in query_values:
#                 query.addBindValue(query_value)

#         query.exec()

#         return query

#     # Параметризованные запросы: Использование ? для защиты от SQL-инъекций.
#     def add_new_transaction_query(self, date, category, description, balance, status):
#         sql_query = "INSERT INTO expenses (Date, Category, Description, Balance, Status) VALUES (?, ?, ?, ?, ?)"
#         self.execute_query_with_params(sql_query, [date, category, description, balance, status])

#     def update_transaction_query(self, date, category, description, balance, status, id):
#         sql_query = "UPDATE expenses SET Date=?, Category=?, Description=?, Balance=?, Status=? WHERE ID=?"
#         self.execute_query_with_params(sql_query, [date, category, description, balance, status, id])

#     def delete_transaction_query(self, id):
#         sql_query = "DELETE FROM expenses WHERE ID=?"
#         self.execute_query_with_params(sql_query, [id])

#     def get_total(self, column, filter=None, value=None):
#         """Динамическое формирование запроса: Для подсчета сумм по категориям. Возвращает строку с символом $ (может вызвать ошибку, если значение NULL)."""
#         sql_query = f"SELECT SUM({column}) FROM expenses"

#         if filter is not None and value is not None:
#             sql_query += f" WHERE {filter} = ?"

#         query_values = []

#         if value is not None:
#             query_values.append(value)

#         query = self.execute_query_with_params(sql_query, query_values)

#         if query.next():
#             return str(query.value(0)) + '$'

#         return '0'

#     def total_balance(self):
#         return self.get_total(column="Balance")

#     def total_income(self):
#         return self.get_total(column="Balance", filter="Status", value="Income")

#     def total_outcome(self):
#         return self.get_total(column="Balance", filter="Status", value="Outcome")

#     def total_groceries(self):
#         return self.get_total(column="Balance", filter="Category", value="Grocery")

#     def total_auto(self):
#         return self.get_total(column="Balance", filter="Category", value="Auto")

#     def total_entertainment(self):
#         return self.get_total(column="Balance", filter="Category", value="Entertainment")

#     def total_other(self):
#         return self.get_total(column="Balance", filter="Category", value="Other")
