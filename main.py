import re
import sqlite3
import sys
from os import startfile, system

import pyttsx3
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QTableWidgetItem

from functional import SET_THEME, THEME, recognize, VOICE, ADD_THEME

tts = pyttsx3.init()
voices = tts.getProperty('voices')

tts.setProperty('voice', 'ru')
sps = []
for voice in voices:
    sps.append(voice.name)

if 'Artemiy' not in sps:
    tts.say('Не установлен мужской голос. Произвожу установку.')
    tts.runAndWait()
    startfile('RHVoice-voice-Russian-Artemiy-v4.0.2009.14-setup.exe')
if 'Tatiana' not in sps:
    tts.say('Не установлен женский голос. Произвожу установку.')
    tts.runAndWait()
    startfile('RHVoice-voice-Russian-Tatiana-v4.0.2009.14-setup.exe')

for voice in voices:
    if voice.name == VOICE:
        tts.setProperty('voice', voice.id)


class EmptyPath(Exception):
    def __init__(self, text):
        self.txt = text


class EmptyCommand(Exception):
    def __init__(self, text):
        self.txt = text


class AllEmpty(Exception):
    def __init__(self, text):
        self.txt = text


class AddWin(QDialog, ADD_THEME):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.add_exit_btn.clicked.connect(self.close)
        self.op_btn_add.clicked.connect(self.search_path)
        self.add_confirm_btn.clicked.connect(self.add_command)
        self._old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return

        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def search_path(self):
        self.path_str.setText(QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0])

    def add_command(self):
        try:
            command = self.command_str.toPlainText()
            path = self.path_str.toPlainText()
            if not command and not path:
                raise AllEmpty('All Empty')
            if not command:
                raise EmptyCommand('Command Empty')
            if not path:
                raise EmptyPath('Path Empty')
            con = sqlite3.connect('commands.sqlite')

            cur = con.cursor()
            try:
                cur.execute(
                    f'''INSERT INTO custom_comands(title, type, puth) VALUES ("{command.lower()}", 8, "{path}")''')
                con.commit()
            except sqlite3.IntegrityError:
                tts.say('Такая команда уже существует.')
                tts.runAndWait()
        except AllEmpty as ae:
            print(ae)
            tts.say('Вы ничего не ввели.')
            tts.runAndWait()
        except EmptyCommand as ec:
            print(ec)
            tts.say('Вы не ввели команду')
            tts.runAndWait()
        except EmptyPath as ep:
            print(ep)
            tts.say('Вы не ввели путь')
            tts.runAndWait()
        self.comand_table.clear()

        labels = ['ID', 'COMMAND', 'PATH']

        self.comand_table.setColumnCount(len(labels))
        self.comand_table.setHorizontalHeaderLabels(labels)

        with sqlite3.connect('commands.sqlite') as connect:
            for id_, command, path in connect.execute("SELECT id, title, puth FROM custom_comands"):
                row = self.comand_table.rowCount()
                self.comand_table.setRowCount(row + 1)

                self.comand_table.setItem(row, 0, QTableWidgetItem(str(id_)))
                self.comand_table.setItem(row, 1, QTableWidgetItem(command))
                self.comand_table.setItem(row, 2, QTableWidgetItem(path))
            for i in range((row + 1) // 2):
                self.comand_table.removeRow(0)


class SetWin(QDialog, SET_THEME):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_exit_btn.clicked.connect(self.close)
        self.confirm_btn.clicked.connect(self.confirm_set)
        self._old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return

        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def confirm_set(self):
        self.status_bar.setText(QtCore.QCoreApplication.translate("Dialog", "     Подтверждаю изменения."))
        with open('setings.txt', 'r+') as f:
            text = f.read()

            if self.white_set_btn.isChecked():
                text = re.sub('black', 'white', text)
                text = re.sub('white', 'white', text)
            elif self.black_set_btn.isChecked():
                text = re.sub('white', 'black', text)
                text = re.sub('black', 'black', text)
            if self.woman_radio_btn.isChecked():
                text = re.sub('man', 'woman', text)
                text = re.sub('woman', 'woman', text)
                text = re.sub('wowoman', 'woman', text)
            elif self.human_radio_btn.isChecked():
                text = re.sub('woman', 'man', text)
                text = re.sub('man', 'man', text)
                text = re.sub('wowoman', 'man', text)
            f.seek(0)
            f.write(text)
            f.truncate()


class MainWin(QMainWindow, THEME):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._old_pos = None
        self.close_but.clicked.connect(self.cls)
        self.settings.clicked.connect(self.open_set)
        self.add_command.clicked.connect(self.open_add)
        self.start_but.clicked.connect(self.run)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return

        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def cls(self):
        sys.exit(app.exec_())

    def open_set(self):
        set_page = SetWin()
        set_page.exec_()

    def open_add(self):
        set_page1 = AddWin()
        set_page1.exec_()

    def run(self):
        tts.say('Произнесите запрос')
        tts.runAndWait()

        inquiry = recognize()
        print(inquiry)
        con = sqlite3.connect('commands.sqlite')

        cur = con.cursor()

        result = cur.execute('SELECT type, puth FROM '
                             '(SELECT * FROM command'
                             ' UNION ALL'
                             ' SELECT * FROM custom_comands)'
                             f' WHERE title="{inquiry.lower()}"')
        index = None
        try:
            for i in result:
                index = i
            if index[0] == 1:
                from datetime import datetime

                a = str(datetime.now().time().strftime('%H %M %S')).split()
                for i in a:
                    if i[0] == '0':
                        i = a[1:]
                tts.say(a[0] + ' часов ' + a[1] + ' минут ' + a[2] + ' секунд')
                tts.runAndWait()
            elif index[0] == 2:
                startfile(index[1])
            elif index[0] == 3:
                startfile("C:\Program Files (x86)\CyberLink\PowerDVD13\PDVDLP.exe")
            elif index[0] == 4:
                system('shutdown /p /f')
            elif index[0] == 5:
                tts.say('Выберите уровень яркости от одного до ста')
                tts.runAndWait()
                level = int(recognize())
                print(level)
                import wmi

                brightness = level  # percentage [0-100] For changing thee screen
                c = wmi.WMI(namespace='wmi')
                methods = c.WmiMonitorBrightnessMethods()[0]
                methods.WmiSetBrightness(brightness, 0)
            elif index[0] == 6:
                from sound import Sound

                cur = Sound.current_volume()  # получили текущие настройки
                tts.say('Выберите уровень громкости от одного до ста')
                tts.runAndWait()
                level = recognize()
                print(level)
                try:
                    Sound.volume_set(int(level))
                except ValueError:
                    if level == 'Выключи звук':
                        Sound.mute()
                    else:
                        tts.say('Некоректные данные. Назовите число от одного до ста.')
                        tts.runAndWait()
            elif index[0] == 7:
                tts.say('В открывшейся папке выберете нужную программу.')
                tts.runAndWait()
                startfile(index[1])
            elif index[0] == 9:
                import webbrowser
                import re
                tts.say('Назовите вводимый запрос')
                tts.runAndWait()
                call = recognize()
                print(call)
                if re.search(r'\.', call):
                    webbrowser.open_new_tab('https://' + call)
                elif re.search(r'\ ', call):
                    webbrowser.open_new_tab('https://www.google.com/search?q=' + call)
                else:
                    webbrowser.open_new_tab('https://www.google.com/search?q=' + call)

            elif index[0] == 8:
                startfile(index[1])
        except TypeError:
            tts.say('Извините не могу вас понять.')
            tts.runAndWait()


sys.setrecursionlimit(5000)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.exit(app.exec_())
