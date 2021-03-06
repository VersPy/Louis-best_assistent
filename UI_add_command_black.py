# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_add_command_black.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sqlite3
from style import add_confirm_btn_black_style, command_str_black_stl, op_btn_add_black_stl, add_exit_btn_balck_stl
from style import command_lable_black_stl, path_lable_black_stl, path_str_black_stl, comand_table_black_stl


class Ui_Add_Command_Black(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(681, 357)
        Dialog.setStyleSheet("background: #1C0460")
        self.add_confirm_btn = QtWidgets.QPushButton(Dialog)
        self.add_confirm_btn.setGeometry(QtCore.QRect(560, 320, 101, 31))
        self.add_confirm_btn.setStyleSheet(add_confirm_btn_black_style)
        self.add_confirm_btn.setObjectName("add_confirm_btn")
        self.command_str = QtWidgets.QTextEdit(Dialog)
        self.command_str.setGeometry(QtCore.QRect(150, 40, 511, 31))
        self.command_str.setStyleSheet(command_str_black_stl)
        self.command_str.setObjectName("command_str")
        self.op_btn_add = QtWidgets.QPushButton(Dialog)
        self.op_btn_add.setGeometry(QtCore.QRect(560, 80, 101, 31))
        self.op_btn_add.setStyleSheet(op_btn_add_black_stl)
        self.op_btn_add.setObjectName("op_btn_add")
        self.add_exit_btn = QtWidgets.QPushButton(Dialog)
        self.add_exit_btn.setGeometry(QtCore.QRect(650, 10, 21, 23))
        self.add_exit_btn.setStyleSheet(add_exit_btn_balck_stl)
        self.add_exit_btn.setObjectName("add_exit_btn")
        self.add_exit_btn.setIcon(QIcon('closer.png'))
        self.add_exit_btn.setIconSize(QSize(10, 10))
        self.command_lable = QtWidgets.QLabel(Dialog)
        self.command_lable.setGeometry(QtCore.QRect(10, 40, 131, 31))
        self.command_lable.setStyleSheet(command_lable_black_stl)
        self.command_lable.setObjectName("command_lable")
        self.path_lable = QtWidgets.QLabel(Dialog)
        self.path_lable.setGeometry(QtCore.QRect(10, 80, 191, 31))
        self.path_lable.setStyleSheet(path_lable_black_stl)
        self.path_lable.setObjectName("path_lable")
        self.path_str = QtWidgets.QTextEdit(Dialog)
        self.path_str.setGeometry(QtCore.QRect(210, 80, 341, 31))
        self.path_str.setStyleSheet(path_str_black_stl)
        self.path_str.setObjectName("path_str")
        self.comand_table = QtWidgets.QTableWidget(Dialog)
        self.comand_table.setGeometry(QtCore.QRect(10, 120, 651, 192))
        self.comand_table.setStyleSheet(comand_table_black_stl)
        self.comand_table.setObjectName("comand_table")
        self.comand_table.horizontalHeader().setHighlightSections(False)
        self.comand_table.horizontalHeader().setStretchLastSection(True)
        self.comand_table.verticalHeader().setVisible(False)
        self.comand_table.clear()

        labels = ['ID', 'COMMAND', 'PATH']

        self.comand_table.setColumnCount(len(labels))
        self.comand_table.setHorizontalHeaderLabels(labels)

        with sqlite3.connect('commands.sqlite') as connect:
            for id_, name, price in connect.execute("SELECT id, title, puth FROM custom_comands"):
                row = self.comand_table.rowCount()
                self.comand_table.setRowCount(row + 1)

                self.comand_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(id_)))
                self.comand_table.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
                self.comand_table.setItem(row, 2, QtWidgets.QTableWidgetItem(price))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add_confirm_btn.setText(_translate("Dialog", "??????????????????????"))
        self.command_str.setText(_translate("Dialog", ""))
        self.op_btn_add.setText(_translate("Dialog", "??????????????"))
        self.add_exit_btn.setText(_translate("Dialog", ""))
        self.command_lable.setText(_translate("Dialog", "      ?????????????? ??????????????:"))
        self.path_lable.setText(_translate("Dialog", "    ???????????????? ???????? ???? ??????????????????:"))
        self.path_str.setText(_translate("Dialog", ""))
