from PyQt5 import QtCore, QtGui, QtWidgets
from sa_library import SQL
import sqlite3

conn = sqlite3.connect("SA.db")
c = conn.cursor()


class Naming_Tables(object):
    def __init__(self, names=[]):
        self.names = names

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(263, 116)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 241, 97))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setBold(False)
        font.setWeight(50)
        self.verticalLayout.addWidget(self.label_2)
        self.rename_input = QtWidgets.QLineEdit(self.widget)
        self.rename_input.setObjectName("rename_input")
        self.verticalLayout.addWidget(self.rename_input)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.enter_name_btn = QtWidgets.QPushButton(self.widget)
        self.enter_name_btn.setObjectName("enter_name_btn")
        self.horizontalLayout.addWidget(self.enter_name_btn)
        self.cancel_btn = QtWidgets.QPushButton(self.widget)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.enter_name_btn.clicked.connect(lambda: self.enter_name(Dialog))
        self.cancel_btn.clicked.connect(Dialog.close)

        self.reveal_default_name(Dialog)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def all_names(self, Dialog):
        '''Gathers all SQLite table names from the SA.db file'''
        c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        for name in c.fetchall():
            self.names.append(name)

    def reveal_default_name(self, Dialog):
        '''Reveals the default 'Sheet1' name given from the pandas conversion function'''
        self.all_names(Dialog)
        default_name = SQL.readable(str(self.names[-1])) #this takes the most recently made table, but when this page operates, "Sheet1" will always be the most recent table
        self.rename_input.setText(default_name)

    def new_table(self, Dialog, tuple, dn):
        '''Replaces the 'Sheet1' table with an identical table, but with a different name, chosen by the user'''
        input = self.rename_input.text()
        new_name = input.replace(" ", "_")
        with conn: #must create a new table, rename the columns with desired name changes, then copy the data from the old table into the new table, drop the old table, then rename this table to the old table's name
            c.execute('CREATE TABLE IF NOT EXISTS backup' + str(tuple)) #creates the correct, corresponding column names of the "new" table
            c.execute("INSERT INTO backup SELECT * FROM {}".format(dn))
            c.execute("DROP TABLE {}".format(dn))
            c.execute("ALTER TABLE backup RENAME TO {}".format(new_name))

    def enter_name(self, Dialog):
        '''Executes the new_table function with a user-chosen name'''
        try:
            if self.rename_input.text() == "":
                raise ValueError
            column_name_list = []
            default_name = SQL.readable(str(self.names[-1]))
            c.execute("SELECT * FROM {}".format(default_name))
            column_names = c.description
            for name in column_names:
                column_name_list.append(name[0])
            column_names = tuple(column_name_list)
            self.new_table(Dialog, column_names, default_name)
            Dialog.close()
        except ValueError:
            pass


    def retranslateUi(self, Dialog):
        '''Translates text from the .ui --> .py conversion'''
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Table Names"))
        self.label.setText(_translate("Dialog", "Do you want to rename your SQLite table?"))
        self.enter_name_btn.setText(_translate("Dialog", "Enter Rename"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Naming_Tables()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    c.close()
    conn.close()
