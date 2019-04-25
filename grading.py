###This is a pop-up page, intended to insert grades for students and customize grading rubrics###

from PyQt5 import QtCore, QtGui, QtWidgets
from sa_library import SQL
import sqlite3

conn = sqlite3.connect("SA.db")
c = conn.cursor()

class Grading_Window(object):

    def __init__(self, name=[], custom_rawscore=[], custom_totalscore=[]):
        '''Initializes only three lists'''
        self.name = name
        self.custom_rawscore = custom_rawscore
        self.custom_totalscore = custom_totalscore

    def setupUi(self, Dialog):
        '''Setup for the GUI'''
        Dialog.setObjectName("Dialog")
        Dialog.resize(422, 283)
        self.exit_btn = QtWidgets.QPushButton(Dialog)
        self.exit_btn.setGeometry(QtCore.QRect(280, 250, 131, 21))
        self.exit_btn.setObjectName("exit_btn")
        self.sql_table_menu = QtWidgets.QComboBox(Dialog)
        self.sql_table_menu.setGeometry(QtCore.QRect(160, 220, 99, 21))
        self.sql_table_menu.setObjectName("sql_table_menu")
        self.sql_table_title = QtWidgets.QLabel(Dialog)
        self.sql_table_title.setGeometry(QtCore.QRect(160, 200, 99, 20))
        self.sql_table_btn = QtWidgets.QPushButton(Dialog)
        self.sql_table_btn.setGeometry(QtCore.QRect(160, 250, 99, 20))
        self.sql_table_btn.setText("Upload Table")
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setBold(True)
        font.setWeight(75)
        self.sql_table_title.setFont(font)
        self.sql_table_title.setObjectName("sql_table_title")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(280, 10, 135, 211))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.new_rubric_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.new_rubric_name.setObjectName("new_rubric_name")
        self.verticalLayout.addWidget(self.new_rubric_name)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.rubric_raw = QtWidgets.QLineEdit(self.layoutWidget)
        self.rubric_raw.setObjectName("rubric_raw")
        self.verticalLayout.addWidget(self.rubric_raw)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.rubric_total = QtWidgets.QLineEdit(self.layoutWidget)
        self.rubric_total.setObjectName("rubric_total")
        self.verticalLayout.addWidget(self.rubric_total)
        self.store_rubric_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.store_rubric_btn.setObjectName("store_rubric_btn")
        self.verticalLayout.addWidget(self.store_rubric_btn)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 135, 211))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rubric_name_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setBold(True)
        font.setWeight(75)
        self.rubric_name_label.setFont(font)
        self.rubric_name_label.setText("")
        self.rubric_name_label.setObjectName("rubric_name_label")
        self.verticalLayout_2.addWidget(self.rubric_name_label)
        self.custom_rubric_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(10)
        self.custom_rubric_label.setFont(font)
        self.custom_rubric_label.setText("")
        self.custom_rubric_label.setObjectName("custom_rubric_label")
        self.verticalLayout_2.addWidget(self.custom_rubric_label)
        self.raw_score_title = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.raw_score_title.setFont(font)
        self.raw_score_title.setObjectName("raw_score_title")
        self.verticalLayout_2.addWidget(self.raw_score_title)
        self.rawscore_input = QtWidgets.QLineEdit(self.layoutWidget1)
        self.rawscore_input.setObjectName("rawscore_input")
        self.verticalLayout_2.addWidget(self.rawscore_input)
        self.calculate_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.calculate_btn.setObjectName("calculate_btn")
        self.verticalLayout_2.addWidget(self.calculate_btn)
        self.total_score_title = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.total_score_title.setFont(font)
        self.total_score_title.setObjectName("total_score_title")
        self.verticalLayout_2.addWidget(self.total_score_title)
        self.total_score_input = QtWidgets.QLineEdit(self.layoutWidget1)
        self.total_score_input.setObjectName("total_score_input")
        self.verticalLayout_2.addWidget(self.total_score_input)
        self.enter_score_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.enter_score_btn.setObjectName("enter_score_btn")
        self.verticalLayout_2.addWidget(self.enter_score_btn)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(160, 100, 101, 98))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.student_menu = QtWidgets.QComboBox(self.layoutWidget2)
        self.student_menu.setObjectName("student_menu")
        self.verticalLayout_3.addWidget(self.student_menu)
        self.column_title = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setBold(True)
        font.setWeight(75)
        self.column_title.setFont(font)
        self.column_title.setObjectName("column_title")
        self.verticalLayout_3.addWidget(self.column_title)
        self.column_menu = QtWidgets.QComboBox(self.layoutWidget2)
        self.column_menu.setObjectName("column_menu")
        self.verticalLayout_3.addWidget(self.column_menu)
        self.layoutWidget3 = QtWidgets.QWidget(Dialog)
        self.layoutWidget3.setGeometry(QtCore.QRect(160, 0, 101, 101))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.rubric_dropdown = QtWidgets.QComboBox(self.layoutWidget3)
        self.rubric_dropdown.setObjectName("rubric_dropdown")
        self.verticalLayout_4.addWidget(self.rubric_dropdown)
        self.choose_rubric_btn = QtWidgets.QPushButton(self.layoutWidget3)
        self.choose_rubric_btn.setObjectName("choose_rubric_btn")
        self.verticalLayout_4.addWidget(self.choose_rubric_btn)
        self.layoutWidget4 = QtWidgets.QWidget(Dialog)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 240, 137, 25))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.misc_input = QtWidgets.QLineEdit(self.layoutWidget4)
        self.misc_input.setObjectName("misc_input")
        self.horizontalLayout.addWidget(self.misc_input)
        self.enter_misc_btn = QtWidgets.QPushButton(self.layoutWidget4)
        self.enter_misc_btn.setObjectName("enter_misc_btn")
        self.horizontalLayout.addWidget(self.enter_misc_btn)

        ####Buttons####

        self.choose_rubric_btn.clicked.connect(lambda: self.choose_rubric(Dialog))
        self.sql_table_btn.clicked.connect(lambda: self.choose_sql_table(Dialog))
        self.store_rubric_btn.clicked.connect(lambda: self.store_rubric(Dialog))
        self.calculate_btn.clicked.connect(lambda: self.calc_btn(Dialog))
        self.enter_score_btn.clicked.connect(lambda: self.enter_total_score(Dialog))
        self.enter_misc_btn.clicked.connect(lambda: self.enter_misc(Dialog))

        self.exit_btn.clicked.connect(Dialog.close)

        self.sql_options(Dialog)
        self.rubric_options(Dialog)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

####Rubric functions####

    def rubric_options(self, Dialog):
        '''Fills rubric menu with rubrics SQLite table'''
        self.rubric_dropdown.addItem("Choose rubric...")
        SQL.menu_add("name", "rubrics", self.rubric_dropdown)

    def rubric_data_extraction(self, Dialog, rubric):
        '''Extracts specific data from selected rubric'''
        SQL.list_add("name", "rubrics", self.name)
        index = self.name.index(rubric) + 1
        SQL.query_list("rawscore", "rubrics", self.custom_rawscore, index)
        SQL.query_list("totalscore", "rubrics", self.custom_totalscore, index)


    def customrubric_label(self, Dialog):
        '''Updates the label for which rubric the user has uploaded from the SQLite table.'''
        try:
            selected_name = self.rubric_dropdown.currentText()
            if selected_name == "":
                raise IndexError
            elif selected_name == "Choose rubric...":
                raise IndexError
            self.rubric_data_extraction(Dialog, selected_name)
            self.custom_rubric_label.setText('x/{} --> x/{}'.format(self.custom_rawscore[0], self.custom_totalscore[0]))
            self.rubric_name_label.setText("{}".format(selected_name))
        except IndexError:
            pass

    def rubric_setup(self, Dialog):
        '''Grabs correct data from SQLite table and stores in lists'''
        try:
            rubric_name = self.rubric_name_label.text()
            if rubric_name == '':
                raise ValueError
            index = self.name.index(rubric_name) + 1
            c.execute("SELECT rawscore, totalscore FROM rubrics WHERE rowid = {}".format(index))
            SQL.query_list("rawscore", "rubrics", self.custom_rawscore, index)
            SQL.query_list("totalscore", "rubrics", self.custom_totalscore, index)
        except ValueError:
            pass

    def choose_rubric(self, Dialog):
        self.clear_score_lists(Dialog)
        self.customrubric_label(Dialog)
        self.rubric_setup(Dialog)


    def r_calc(self, Dialog, input, sql_raw, sql_total):
        '''This is a calculator for the custom rubric'''
        if type(input) not in [int, float]:
            raise TypeError("Must be a number")
        elif input < 0:
            raise ValueError("Must be greater than 0")
        result = round((input / sql_raw) * sql_total, 2) #algorithym for grading rubric
        return result

    def score_calculated(self, Dialog):
        '''Displays calculated score on the Total Score line edit'''
        try:
            rawscore = float(self.rawscore_input.text()) #converts textbox data into a REAL number for the algorithym below
            int_raw = int(self.custom_rawscore[-1]) #in case of any unexpected data, this will only grab the last (and only relevant) item in the list
            int_total = int(self.custom_totalscore[-1])
            result = self.r_calc(Dialog, rawscore, int_raw, int_total)
            self.total_score_input.setText(str(result)) #reveals the result of the algorithym to the user
        except ValueError:
            pass
        except TypeError:
            pass

    def calc_btn(self, Dialog):
        self.score_calculated(Dialog)
        self.rawscore_input.clear()

    def refresh(self, Dialog):
        '''When a new rubric is created, this clears the input boxes and refreshes the rubric menu.'''
        self.rubric_raw.clear()
        self.rubric_total.clear()
        self.new_rubric_name.clear()
        self.rubric_dropdown.clear()
        self.rubric_options(Dialog)

    def store_rubric(self, Dialog):
        '''Stores custom rubric info in SQLite table'''
        try:
            raw = self.rubric_raw.text()
            total = self.rubric_total.text()
            name = self.new_rubric_name.text()
            if raw == "":
                raise sqlite3.OperationalError
            elif total == "":
                raise sqlite3.OperationalError
            elif name == "":
                raise sqlite3.OperationalError
            else:
                with conn:
                    c.execute("INSERT INTO rubrics (name, rawscore, totalscore) VALUES (?, ?, ?)", (name, raw, total))
                self.refresh(Dialog)
        except sqlite3.OperationalError:
            pass

    def enter_grades(self, Dialog, input):
        '''The input parameter is for total_score_input or misc_input'''
        try:
            if input == "":
                raise sqlite3.OperationalError
            student_names = []
            table = self.sql_table_menu.currentText()
            student = self.student_menu.currentText().replace("(", "").replace(")", "")
            column = self.column_menu.currentText()
            SQL.list_add("Students", table, student_names)
            readable = SQL.readable_list(student_names)
            inx = readable.index(student) + 1
            with conn: #this enters data for any student and in any column the user wants
                c.execute("UPDATE {} SET {} = {} WHERE rowid = {}".format(table, column, input, inx))
            student_names.clear()
        except sqlite3.OperationalError:
            pass

    def enter_total_score(self, Dialog):
        '''For the Total Score button'''
        self.enter_grades(Dialog, self.total_score_input.text())
        self.total_score_input.clear()

    def enter_misc(self, Dialog):
        '''For the Misc Input button'''
        self.enter_grades(Dialog, self.misc_input.text())
        self.misc_input.clear()

####Non-rubric functions####

    def sql_options(self, Dialog):
        '''Fills the SQLite table menu'''
        self.sql_table_menu.addItem("Choose table...")
        SQL.tables_info(self.sql_table_menu)

    def choose_sql_table(self, Dialog):
        '''Inserts data into student menu and column menu from the SQLite table chosen by the user'''
        try:
            self.student_menu.clear()
            self.column_menu.clear()
            SQL.menu_add("Students", self.sql_table_menu.currentText(), self.student_menu)
            SQL.menu_add_cols(self.sql_table_menu.currentText(), self.column_menu)
        except sqlite3.OperationalError:
            pass

    def clear_score_lists(self, Dialog):
        '''Clears the lists defined in the __init__ function'''
        self.name.clear()
        self.custom_rawscore.clear()
        self.custom_totalscore.clear()


    def retranslateUi(self, Dialog):
        '''Translates text from the .ui --> .py conversion'''
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Grading"))
        self.exit_btn.setText(_translate("Dialog", "Exit"))
        self.sql_table_title.setText(_translate("Dialog", "SQLite Table"))
        self.label_7.setText(_translate("Dialog", "Custom Rubric:"))
        self.label_10.setText(_translate("Dialog", "Rubric Name:"))
        self.label_8.setText(_translate("Dialog", "Raw Score:"))
        self.label_9.setText(_translate("Dialog", "Total Score:"))
        self.store_rubric_btn.setText(_translate("Dialog", "Store Rubric"))
        self.raw_score_title.setText(_translate("Dialog", "Raw Score:"))
        self.calculate_btn.setText(_translate("Dialog", "Calculate"))
        self.total_score_title.setText(_translate("Dialog", "Total Score:"))
        self.enter_score_btn.setText(_translate("Dialog", "Enter Score"))
        self.label_4.setText(_translate("Dialog", "Student"))
        self.column_title.setText(_translate("Dialog", "Column"))
        self.label_6.setText(_translate("Dialog", "Grading Rubrics"))
        self.choose_rubric_btn.setText(_translate("Dialog", "Choose Rubric"))
        self.enter_misc_btn.setText(_translate("Dialog", "Enter Misc..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Grading_Window()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    c.close()
    conn.close()
