import sys
#import jsonpickle
#jsonpickle.set_encoder_options('json', indent=4)
#jsonpickle.set_encoder_options('simplejson', indent=4)
import io
import os

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * #QMainWindow, QDialog, QGraphicsScene, QListWidget, QListWidgetItem, QApplication, QSizePolicy
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6 import uic

import match as core

class MainWindow(QMainWindow):
    def __init__(self, core):
        self.file_name = None

        QMainWindow.__init__(self)
        self.core = core

        #Window code
        self.ui = uic.loadUi('./ui/MainWindow.ui')
        self.setCentralWidget(self.ui)
        #self.changeTitle()
        self.resize(800, 600)

        self.ui.pb_add_player.clicked.connect(
            lambda: self.add_player(self.ui.le_player_name.text()))
        self.ui.le_player_name.returnPressed.connect(
            lambda: self.add_player(self.ui.le_player_name.text()))

        self.ui.lv_players.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.lv_players.customContextMenuRequested.connect(
            self.lv_players_rightclick_menu)

    def lv_players_rightclick_menu(self, position):
        #Popup menu
        pop_menu = QMenu()
        delete_player_action = QAction('Remove player',self)
        rename_player_action = QAction('Rename player', self)
        #Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        pop_menu.addAction(delete_player_action)
        if self.ui.lv_players.itemAt(position):
            pop_menu.addAction(rename_player_action)

        rename_player_action.triggered.connect(self.lva_rename_player)
        delete_player_action.triggered.connect(self.lva_remove_player)
        pop_menu.exec(self.ui.lv_players.mapToGlobal(position))

    #Delete group
    def lva_remove_player(self):
        player = self.ui.lv_players.currentItem().data(Qt.ItemDataRole.UserRole)
        self.confirm(
            'Remove {}?'.format(player.name),
            'Confirm player removal'
        )
        self.remove_player(player.name)
        self.ui.lv_players.takeItem(self.ui.lv_players.currentRow())

    #Renaming group
    #TODO
    def lva_rename_player(self):
        curRow = self.ui.lv_players.currentRow()
        item = self.ui.lv_players.item(curRow)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.ui.lv_players.editItem(item)

        def try_rename_player(*nargs):
            player = self.ui.lv_players.currentItem().data(Qt.ItemDataRole.UserRole)
            core.rename_player(player.name, new_name)


        self.ui.lv_players.itemChanged.connect(lambda *x: try_rename_player(x))

    def add_player(self, player_name):
        #player_name = self.ui.le_player_name.text()
        player = core.add_player(player_name)
        if player:
            list_item = QListWidgetItem(player.name)
            list_item.setData(Qt.ItemDataRole.UserRole, player)
            self.ui.lv_players.addItem(list_item)

    def remove_player(self, player_name):
        core.remove_player(player_name)

    def confirm(self, message, title=''):
        reply = QMessageBox()
        #Force cancel left and OK right
        reply.setStyleSheet('*{button-layout: 3}')
        reply.setText(message)
        reply.setWindowTitle(title)
        reply.setStandardButtons(
            QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)

        x = reply.exec()

        return x == QMessageBox.StandardButton.Ok

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow(None)
    window.show()

    app.exec()
    sys.exit(app.exit())
    #app.exec_()
    #sys.exit(app.exit())