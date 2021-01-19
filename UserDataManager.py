import sys
import json
import os
from PyQt5.QtWidgets import QPushButton, QApplication, QMainWindow, QLineEdit, QWidget
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
import main_menu

SCREEN_SIZE = [660, 660]


def get_user_data():
    try:
        open(os.path.join('data', 'users.json'), 'r', encoding='utf8')
    except FileNotFoundError:
        with open(os.path.join('data', 'users.json'), 'w', encoding='utf8') as f:
            print('{}', file=f)

    with open(os.path.join('data', 'users.json'), 'r', encoding='utf8') as input_file:
        d = json.load(input_file)
    return d


def get_user_levels():
    with open(os.path.join('data', 'unlock_levels.json'), 'r', encoding='utf8') as input_file:
        d = json.load(input_file)
    return d


def put_user_data(users_list):
    with open(os.path.join('data', 'users.json'), 'w', encoding='utf8') as output_file:
        json.dump(users_list, output_file)


def put_user_levels(users_levels):
    with open(os.path.join('data', 'unlock_levels.json'), 'w', encoding='utf8') as output_file:
        json.dump(users_levels, output_file)


class UserDataManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Textorcist')
        self.setFixedSize(*SCREEN_SIZE)

        oImage = QImage(os.path.join('data', 'main_menu_background'))
        sImage = oImage.scaled(QSize(*SCREEN_SIZE))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.btn_play = QPushButton('ВОЙТИ', self)
        self.btn_play.move(260, 490)
        self.btn_play.resize(140, 70)
        self.btn_play.clicked.connect(self.login)

        self.btn_exit = QPushButton('РЕГИСТРАЦИЯ', self)
        self.btn_exit.move(260, 581)
        self.btn_exit.resize(140, 70)
        self.btn_exit.clicked.connect(self.register)

        self.show()

    def login(self):
        self.close()
        self.ex = Login()
        self.ex.show()

    def register(self):
        self.close()
        self.ex = Register()
        self.ex.show()


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Textorcist')
        self.setFixedSize(*SCREEN_SIZE)

        oImage = QImage(os.path.join('data', 'main_menu_background'))
        sImage = oImage.scaled(QSize(*SCREEN_SIZE))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.user_login = QLineEdit(self)
        self.user_login.setPlaceholderText('ЛОГИН')
        self.user_login.move(260, 420)

        self.user_pass = QLineEdit(self)
        self.user_pass.setPlaceholderText('ПАРОЛЬ')
        self.user_pass.move(260, 450)

        self.btn_play = QPushButton('ВОЙТИ', self)
        self.btn_play.move(257, 490)
        self.btn_play.resize(140, 70)
        self.btn_play.clicked.connect(self.login)

        self.btn_back = QPushButton('НАЗАД', self)
        self.btn_back.move(257, 580)
        self.btn_back.resize(140, 70)
        self.btn_back.clicked.connect(self.back)

        self.show()

    def login(self):
        login = self.user_login.text()
        password = self.user_pass.text()
        print('ВХОД', login, password)

        users_list = get_user_data()

        if login in users_list:
            if users_list[login] == password:
                self.close()
                with open('player_name.txt', 'w', encoding='utf8') as output_file:
                    output_file.write(login)
                self.ex = main_menu.MainMenu()
                self.ex.show()
                return
        print('Нет такого аккаунта')

    def back(self):
        self.close()
        self.ex = UserDataManager()
        self.ex.show()


class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Textorcist')
        self.setFixedSize(*SCREEN_SIZE)

        oImage = QImage(os.path.join('data', 'main_menu_background'))
        sImage = oImage.scaled(QSize(*SCREEN_SIZE))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.user_login = QLineEdit(self)
        self.user_login.setPlaceholderText('ЛОГИН')
        self.user_login.move(260, 420)

        self.user_pass = QLineEdit(self)
        self.user_pass.setPlaceholderText('ПАРОЛЬ')
        self.user_pass.move(260, 450)

        self.btn_play = QPushButton('РЕГИСТРАЦИЯ', self)
        self.btn_play.move(257, 490)
        self.btn_play.resize(140, 70)
        self.btn_play.clicked.connect(self.reg)

        self.btn_back = QPushButton('НАЗАД', self)
        self.btn_back.move(257, 580)
        self.btn_back.resize(140, 70)
        self.btn_back.clicked.connect(self.back)

        self.show()

    def reg(self):
        login = self.user_login.text()
        password = self.user_pass.text()
        print('Рега', login, password)

        users_list = get_user_data()
        users_levels = get_user_levels()

        if login not in users_list:
            users_list[login] = password
            users_levels[login] = list()
            users_levels[login].append('level_1')
            put_user_data(users_list)
            put_user_levels(users_levels)
            print('New_user: ', login, password)
        else:
            print('Логин занят')

    def back(self):
        self.close()
        self.ex = UserDataManager()
        self.ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pril = UserDataManager()
    sys.exit(app.exec())
