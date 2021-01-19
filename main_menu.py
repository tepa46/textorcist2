import sys
from PyQt5.QtWidgets import QInputDialog, QPushButton, QApplication, QWidget
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
import game_file
import UserDataManager
import game_info

SCREEN_SIZE = [660, 660]


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Textorcist')
        self.setFixedSize(*SCREEN_SIZE)

        oImage = QImage('data/main_menu_background')
        sImage = oImage.scaled(QSize(*SCREEN_SIZE))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.btn_play = QPushButton('ИГРАТЬ', self)
        self.btn_play.move(260, 490)
        self.btn_play.resize(140, 70)
        self.btn_play.clicked.connect(self.play)

        self.btn_exit = QPushButton('Сменить аккаунт', self)
        self.btn_exit.move(260, 581)
        self.btn_exit.resize(140, 70)
        self.btn_exit.clicked.connect(self.back)

        self.show()

    def play(self):
        open('game_info.py')
        player_name = game_info.info.player_name
        levels = UserDataManager.get_user_levels()
        level, ok_pressed = QInputDialog.getItem(
            self, "Выбор уровня", "Выберите уровень или напишите его название",
            levels[player_name], 0, False)
        if ok_pressed:
            game_info.info.clear_files()
            game_info.info.put_level(level)
            game_info.info.init_all_info()
            self.setFixedSize(0, 0)
            game_file.Textorcist()
            self.setFixedSize(*SCREEN_SIZE)

    def back(self):
        self.close()
        self.ex = UserDataManager.UserDataManager()
        self.ex.show()


def main():
    pril = MainMenu()
    pril.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec())
