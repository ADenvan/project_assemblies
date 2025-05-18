import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtSql import QSqlTableModel

from ui_main import Ui_MainWindow
from new_transaction import Ui_Dialog
from connection import Data
"""Импорт системных модулей (sys) для работы с аргументами командной строки.
PySide6 модули для GUI и работы с БД:
QtWidgets - базовые виджеты.
QApplication - главный класс приложения.
QMainWindow - окно главного интерфейса.
QSqlTableModel - модель для отображения табличных данных из БД.
Пользовательские UI-классы (Ui_MainWindow, Ui_Dialog), сгенерированные Qt Designer.
"""

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super(ExpenseTracker, self).__init__()
        self.ui = Ui_MainWindow()  # Инициализация интерфейса
        self.ui.setupUi(self)      # Настройка виджетов
        self.conn = Data()        # Подключение к Б
        self.view_data()           # Загрузка данных в таблицу
        self.reload_data()         # Обновление статистики

        # Привязка кнопок к методам
        self.ui.btn_new_transaction.clicked.connect(self.open_new_transaction_window)
        self.ui.btn_edit_transaction.clicked.connect(self.open_new_transaction_window)
        self.ui.btn_delete_transaction.clicked.connect(self.delete_current_transaction)

    def reload_data(self):
        """Цель: Обновление статистики в интерфейсе.
            Вызовы методов Data: total_balance() - общий баланс. total_income()/total_outcome() - доходы/расходы. Категории (total_groceries(), total_auto() и т.д.)."""
        self.ui.current_balance.setText(self.conn.total_balance())
        self.ui.income_balance.setText(self.conn.total_income())
        self.ui.outcome_balance.setText(self.conn.total_outcome())
        self.ui.total_groceries.setText(self.conn.total_groceries())
        self.ui.total_auto.setText(self.conn.total_auto())
        self.ui.total_entertainment.setText(self.conn.total_entertainment())
        self.ui.total_other.setText(self.conn.total_other())

    def view_data(self):
        """QSqlTableModel: Автоматически синхронизируется с БД. Метод select() выполняет SQL-запрос SELECT * FROM expenses."""
        self.model = QSqlTableModel(self)  # Создание модели
        self.model.setTable('expenses')    # Привязка к таблице БД
        self.model.select()                # Загрузка данных
        self.ui.tableView.setModel(self.model)  # Связь с виджетом

    def open_new_transaction_window(self):
        """Динамическое окно: Создается при каждом вызове. Определение отправителя: Проверка текста кнопки для выбора действия."""
        self.new_window = QtWidgets.QDialog()     # Создание диалога
        self.ui_window = Ui_Dialog()              # Инициализация UI
        self.ui_window.setupUi(self.new_window)   # Настройка виджетов
        self.new_window.show()                    # Показ окна

        # Определение действия кнопки (Добавить/Изменить)
        sender = self.sender()
        if sender.text() == "New transaction":
            self.ui_window.btn_new_transaction.clicked.connect(self.add_new_transaction)
        else:
            self.ui_window.btn_new_transaction.clicked.connect(self.edit_current_transaction)

    def add_new_transaction(self):
        """Сбор данных: Из виджетов диалогового окна. Метод add_new_transaction_query() выполняет SQL-запрос INSERT."""
        # Получение данных из полей ввода
        date = self.ui_window.dateEdit.text()
        category = self.ui_window.cb_choose_category.currentText()
        description = self.ui_window.le_description.text()
        balance = self.ui_window.le_balance.text()
        status = self.ui_window.cb_status.currentText()

        # Вызов метода добавления в БД
        self.conn.add_new_transaction_query(date, category, description, balance, status)
        self.view_data()       # Обновление таблицы
        self.reload_data()     # Обновление статистики
        self.new_window.close()  # Закрытие окна

    def edit_current_transaction(self):
        """Получение ID: Из выделенной строки таблицы. Метод update_transaction_query() выполняет SQL-запрос UPDATE."""
        index = self.ui.tableView.selectedIndexes()[0] # Выбранная строка
        id = str(self.ui.tableView.model().data(index)) # ID записи

        # Получение новых данных
        date = self.ui_window.dateEdit.text()
        category = self.ui_window.cb_choose_category.currentText()
        description = self.ui_window.le_description.text()
        balance = self.ui_window.le_balance.text()
        status = self.ui_window.cb_status.currentText()
        
        # Вызов метода обновления в БД
        self.conn.update_transaction_query(date, category, description, balance, status, id)
        self.view_data()
        self.reload_data()
        self.new_window.close()

    def delete_current_transaction(self):
        """Метод delete_transaction_query() выполняет SQL-запрос DELETE."""
        index = self.ui.tableView.selectedIndexes()[0]  # Выбранная строка
        id = str(self.ui.tableView.model().data(index)) # ID записи

        self.conn.delete_transaction_query(id)  # Удаление записи
        self.view_data()
        self.reload_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()

    sys.exit(app.exec())
