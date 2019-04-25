import sqlite3
import os
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from sa_library import *
from table_naming import Naming_Tables
from grading import Grading_Window

class Window(QtWidgets.QMainWindow): #window for Qt designer
    def __init__(self, sql_dict={}, exl_dict={}, sources=[], sources_t2=[], columns=[], columns_t2=[], x_prep=[], y_prep=[], means=[]):
        self.sql_dict = sql_dict #these data structures are mostly used for the graph functions on Tab 1 and the table functions on Tab 2
        self.exl_dict = exl_dict
        self.sources = sources
        self.sources_t2 = sources_t2
        self.columns = columns
        self.columns_t2 = columns_t2
        self.x_prep = x_prep
        self.y_prep = y_prep
        self.means = means

        super(Window, self).__init__()
        uic.loadUi('SA.ui', self) #load UI file we have been working on in Qt designer
        self.setWindowTitle('Student Analyser')
        self.setWindowIcon(QtGui.QIcon("icon/ta_icon.png"))
        self.default_tables()

#TAB 1 buttons

        self.choose_source_btn.clicked.connect(self.choose_source)
        self.remove_source_btn.clicked.connect(self.remove_source)
        self.add_source_btn.clicked.connect(self.add_source)
        self.select_source_btn.clicked.connect(self.select_source)
        self.add_student_btn.clicked.connect(lambda: self.student_or_column(self.student_menu_t1.currentText()))
        self.add_column_data_btn.clicked.connect(lambda: self.student_or_column(self.column_menu_t1.currentText()))
        self.remove_student_btn.clicked.connect(self.remove_student)
        self.remove_column_btn.clicked.connect(self.remove_column)

        self.bar_graph_btn.clicked.connect(self.bar_graph_final)
        self.line_graph_btn.clicked.connect(self.line_graph_final)
        self.pie_chart_btn.clicked.connect(self.pie_chart_final)

        self.exit_btn_t1.clicked.connect(self.close)


###Tab 2 buttons

        self.sql_options()
        self.exl_options()

        self.search_file_btn.clicked.connect(self.search_file)
        self.upload_excel_btn.clicked.connect(self.upload_exl_1)
        self.convert_sqlite_btn.clicked.connect(self.exl_to_sql)
        self.use_exl_btn.clicked.connect(self.upload_exl_2)
        self.use_sql_btn.clicked.connect(self.upload_sql)
        self.show_info_btn.clicked.connect(self.show_info)
        self.add_columns_btn.clicked.connect(self.add_column_t2)
        self.remove_column_btn_2.clicked.connect(self.remove_column_t2)

        self.clear_table_btn.clicked.connect(self.clear_table)
        self.grading_page_btn.clicked.connect(lambda: self.other_windows(Grading_Window()))
        self.exit_btn_t2.clicked.connect(self.close)


    def default_tables(self):
        '''Automatically creates a SQLite table for custom grading rubrics and excel file paths'''
        with conn:
            c.execute("CREATE TABLE IF NOT EXISTS rubrics(name TEXT, rawscore TEXT, totalscore TEXT)") #for grading rubrics
            c.execute("CREATE TABLE IF NOT EXISTS excel_paths(path TEXT)") #for excel files

    def other_windows(self, page):
        '''This is to open the Naming_Tables and Grading_Window pages'''
        self.err_t2.setText("")
        self.window = QtWidgets.QDialog()
        page.setupUi(self.window)
        self.window.show()

########################TAB 1#########################

    def dict_additions(self, dict, source, student):
        '''Data from SQlite tables and Excel files will be separated using dictionaries'''
        dict.setdefault(source, []).append(student)

    def boxes_checked(self, sql_query):
        '''This function will look for either excel paths or SQLite tables'''
        raw_sources = []
        sql = sql_query
        for source in c.fetchall():
            raw_sources.append(source)
        readable = SQL.readable_list(raw_sources)
        sources = [i for i in readable if i not in ("rubrics", "excel_paths")] #filters out irrelevant sqlite tables
        for source in sources:
            self.source_menu.addItem("{}".format(source))

    def choose_source(self):
        '''Fills the sources menu with sources from Excel files, SQLite tables, or both'''
        self.source_menu.clear()
        self.err_t1.setText("")
        self.source_menu.addItem("Choose source...")
        if self.sqlite_box.isChecked() and self.excel_box.isChecked():
            self.boxes_checked(c.execute("SELECT name FROM sqlite_master WHERE type = 'table'"))
            self.boxes_checked(c.execute("SELECT path FROM excel_paths"))
        elif self.sqlite_box.isChecked():
            self.boxes_checked(c.execute("SELECT name FROM sqlite_master WHERE type = 'table'"))
        elif self.excel_box.isChecked():
            self.boxes_checked(c.execute("SELECT path FROM excel_paths"))
        else:
            self.err_t1.setText("Choose a source type")

    def add_source(self):
        '''Adds items from the source_menu to data_source_view (list widget)'''
        try:
            self.err_t1.setText("")
            source = self.source_menu.currentText()
            if source == "Choose source...":
                raise ValueError
            elif source == "":
                raise NameError
            self.data_source_view.addItem(source)
            self.data_source_view.setCurrentRow(0)
        except ValueError:
            self.err_t1.setText("Choose a data source")
        except NameError:
            self.err_t1.setText("Choose SQLite and/or Excel data sources")

    def remove_source(self):
        '''Removes items from the data_source_view'''
        try:
            self.err_t1.setText("")
            selected = self.data_source_view.currentRow()
            self.data_source_view.takeItem(selected)
        except AttributeError:
            self.err_t1.setText("Not a source")

    def exl_students(self):
        '''Fills the student menu with Excel data'''
        row = self.data_source_view.currentRow()
        selected = self.data_source_view.item(row)
        path = selected.text()
        Excel.menu_add(path, "Students", self.student_menu_t1)

    def exl_columns(self):
        '''Fills the columns menu with Excel data'''
        row = self.data_source_view.currentRow()
        selected = self.data_source_view.item(row)
        path = selected.text()
        Excel.menu_add_cols(path, "Students", self.column_menu_t1)

    def exl_source(self):
        self.student_menu_t1.clear()
        self.column_menu_t1.clear()
        self.exl_students()
        self.exl_columns()

    def sql_students_t1(self):
        '''Fills the student menu with data from SQLite tables'''
        self.student_menu_t1.addItem("Choose...")
        SQL.menu_add("Students", self.sources[-1], self.student_menu_t1)

    def sql_columns_t1(self):
        '''Fills the columns menu with data from SQLite tables'''
        self.column_menu_t1.addItem("Choose...")
        SQL.menu_add_cols(self.sources[-1], self.column_menu_t1)

    def sql_source(self):
        '''Functions combined for button'''
        self.student_menu_t1.clear()
        self.column_menu_t1.clear()
        self.sql_students_t1()
        self.sql_columns_t1()

    def select_source(self):
        '''For the 'Select Source' button'''
        try:
            self.err_t1.setText("")
            row = self.data_source_view.currentRow()
            selected = self.data_source_view.item(row).text()
            self.sources.append(selected)
            if ".xlsx" in selected:
                self.exl_source()
            else:
                self.sql_source()
        except AttributeError:
            self.err_t1.setText("Choose a data source")

    def student_or_column(self, selected): #the selected parameter is either student_menu_t1 or column_menu_t1
        '''This is to put a selected item into a list widget and add it, if it's a student, to a dictionary'''
        try:
            self.err_t1.setText("")
            if selected == "":
                raise NameError
            elif selected == "Choose...":
                raise ValueError
            else:
                if selected == self.student_menu_t1.currentText(): #if item from student menu is selected
                    self.students_view.addItem(selected)
                    self.students_view.setCurrentRow(0)
                    if ".xlsx" in self.sources[-1]: #if uploaded source is an Excel file
                        self.dict_additions(self.exl_dict, self.sources[-1], selected)
                    else: #if uploaded source is a SQLite table
                        self.dict_additions(self.sql_dict, self.sources[-1], selected)
                elif selected == self.column_menu_t1.currentText(): #if item from column menu is selected
                    self.column_view_t1.addItem(selected)
                    self.column_view_t1.setCurrentRow(0)
        except NameError:
            self.err_t1.setText("Select source in the list-box")
        except ValueError:
            self.err_t1.setText("Not a valid choice")

    def remove_column(self):
        '''Removes a column from the column_view list widget'''
        self.err_t1.setText("")
        selected = self.column_view_t1.currentRow()
        self.column_view_t1.takeItem(selected)

    def remove_student(self):
        '''Removes a student from the students_view list widget AND removes them from their respective dictionaries'''
        try:
            self.err_t1.setText("")
            selected = self.students_view.currentRow()
            student = self.students_view.item(selected).text()
            self.rem_dict_student(self.sql_dict, student) #removes from dictionary
            self.rem_dict_student(self.exl_dict, student)
            self.students_view.takeItem(selected) #removes from list widget
        except AttributeError:
            self.err_t1.setText("Not a student")

    def rem_dict_student(self, dict, student):
        '''Removes a student from their respective dictionaries'''
        for i in dict.values():
            if student in i:
                i.remove(student)

#####GRAPHS#####

    def bar_display(self, col):
        '''Displays the bar graph visuals'''
        plt.xlabel('Student')
        plt.xticks(fontsize=5, rotation=10)
        plt.ylabel('{} score'.format(col))
        plt.title('Student-Student Comparison')
        plt.show()

    def bar_graph_1(self, x, y, c):
        '''Inputs data and completes the graph function, excluding the mean(s)'''
        for xx, yy in zip(x, y):
            plt.bar(xx, yy, color='green')
        self.bar_display(c)

    def bar_graph_2(self, x, y, c, m): #'c' parameter is for the self.columns list
        '''Same as the function above, but includes the mean(s)'''
        for xx, yy in zip(x, y): #normal data
            plt.bar(xx, yy, color='green')
        for xx, yy in m: #for the mean(s)
            plt.bar(xx, yy, color="black")
        self.bar_display(c)

    def line_display(self):
        '''Displays the line graph visuals'''
        plt.xlabel('Assignments or Tests')
        plt.xticks(fontsize=8, rotation=5)
        plt.ylabel('Grades')
        plt.title('Grade Progression')
        plt.legend(loc=5, prop={"size":8})
        plt.show()

    def line_graph_1(self, x, y):
        '''Inputs data and completes the line graph function, excluding the mean(s)'''
        for i, ii in y:
            plt.plot(x, ii, label=i)
        self.line_display()

    def line_graph_2(self, x, y, z):
        '''Same as the function above, but includes the mean(s)'''
        for i, ii in y:
            plt.plot(x, ii, label=i)
        for i, ii in z: #for the mean of each source
            plt.plot(x, ii, label=i)
        self.line_display()

    def pie_info(self, pct, allvals):
        '''Shows text data on the pie chart'''
        absolute = int(pct / 100.*np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    def pie_graph(self, zipped_data):
        '''Completes the pie chart function'''
        for title, data in zipped_data:
            chart = plt.pie(data,
                            labels=self.columns,
                            autopct=lambda pct: self.pie_info(pct, data),
                            shadow=True)
            plt.title(title) #student name
            plt.show()

    def sql_bar_graph(self):
        '''All of the backend work, gathering data for the bar graph function using data from SQLite tables'''
        students = [] #temporary lists to hold data
        indexes = []
        names = []
        raw_data = []
        if len(self.sql_dict) > 0:
            for db in self.sql_dict: #for each key in the sql dictionary
                SQL.list_add("students", db, students)
                for name in self.sql_dict[db]: #for each value (Student) in said key
                    inx = students.index(name) + 1
                    indexes.append(inx)
                    names.append(name)
                for i in indexes:
                    SQL.query_list(self.columns[0], db, raw_data, i) #stores specific data for each student in the dictionary key
                readable = SQL.readable_list(raw_data)
                students.clear()
                indexes.clear()
            d = ["0" if i=="-" else i for i in readable] #to prepare for float conversion
            self.y_prep.append([float(i) for i in d]) #prepares data for the y-axis of the bar graph
            self.x_prep.append([i.strip("1234567890- ") for i in names]) #prepares data for the x-axis of the bar graph
        else: #if no keys in the sql dictionary, just skip the function
            pass

    def exl_bar_graph(self):
        '''Same purpose as the function above, but for extracting data from Excel files'''
        headers = []
        names = []
        data = []
        if len(self.exl_dict) > 0:
            for path in self.exl_dict:
                workbook = xlrd.open_workbook(path)
                sheet = workbook.sheet_by_index(0)
                for header in range(sheet.ncols):
                    headers.append(sheet.cell_value(0, header))
                inx = headers.index(self.columns[0])
                students = Excel.data_list(sheet, 0)
                grades = Excel.data_list(sheet, inx)
                for name in self.exl_dict[path]:
                    names.append(name)
                    inx2 = students.index(name)
                    data.append(grades[inx2])
                students.clear()
                grades.clear()
                headers.clear()
            d = ["0" if i=="-" else i for i in data]
            self.x_prep.append([i.strip("1234567890- ") for i in names])
            self.y_prep.append([float(i) for i in d])
        else:
            pass

    def sql_lp_graph(self):
        '''This backend function for extracting data from SQLite tables is used for both the line graph and the pie chart'''
        names = []
        students = []
        indexes = []
        data = []
        if len(self.sql_dict) > 0:
            for db in self.sql_dict:
                SQL.list_add("students", db, students)
                for name in self.sql_dict[db]:
                    inx = students.index(name) + 1
                    indexes.append(inx)
                    names.append(name)
                for i in indexes:
                    for column in self.columns:
                        SQL.query_list(column, db, data, i)
                    readable = SQL.readable_list(data)
                    d = ["0" if i=="-" else i for i in readable]
                    self.y_prep.append([float(i) for i in d])
                    data.clear()
                students.clear()
                indexes.clear()
            self.x_prep.append([i.strip("1234567890- ") for i in names])
        else:
            pass

    def exl_lp_graph(self):
        '''Same purpose as the function above, but for Excel files'''
        headers = []
        names = []
        data = []
        if len(self.exl_dict) > 0:
            for path in self.exl_dict:
                workbook = xlrd.open_workbook(path)
                sheet = workbook.sheet_by_index(0)
                Excel.list_add_cols(path, headers)
                students = Excel.data_list(sheet, 0)
                for name in self.exl_dict[path]:
                    names.append(name)
                    inx = students.index(name)
                    for column in self.columns:
                        inx2 = headers.index(column)
                        grades = Excel.data_list(sheet, inx2)
                        data.append(grades[inx])
                    d = ["0" if i=="-" else i for i in data]
                    self.y_prep.append([float(i) for i in d])
                    data.clear()
                grades.clear()
                headers.clear()
            self.x_prep.append([i.strip("1234567890- ") for i in names])
        else:
            pass

    def sql_means(self):
        '''Finds the mean of columns selected from SQLite sources'''
        averages = []
        data = []
        for db in self.sql_dict:
            for column in self.columns:
                SQL.list_add(column, db, data)
                d = ["0" if i=="-" else i for i in data]
                floats = [float(i) for i in d]
                data.clear()
                averages.append(round(np.mean(floats), 2))
            self.means.append([i for i in averages])
            averages.clear()

    def exl_means(self):
        '''Finds the mean of columns selected from .xlsx files'''
        averages = []
        headers = []
        for path in self.exl_dict:
            workbook = xlrd.open_workbook(path)
            sheet = workbook.sheet_by_index(0)
            Excel.list_add_cols(path, headers)
            for column in self.columns:
                inx = headers.index(column)
                data = Excel.data_list(sheet, inx)
                data.remove(column)
                d = ["0" if i=="-" else i for i in data]
                grades = [float(i) for i in d]
                averages.append(round(np.mean(grades), 2))
            self.means.append([i for i in averages])
            averages.clear()
            headers.clear()

    def clear_house(self):
        '''Clears the lists used for storing data utilized by the backend graph functions'''
        self.x_prep.clear()
        self.y_prep.clear()
        self.means.clear()

    def axis_and_bar_graph(self):
        '''These 'axis' functions prepare data for finalized graph functions. This is for the bar graph functions'''
        x_axis = []
        y_axis = []
        m_sources = []
        means2 = []
        Graphs.inception(self.x_prep, x_axis)
        Graphs.inception(self.y_prep, y_axis)
        if self.bar_mean_box.isChecked():
            Graphs.means_labels(self.sql_dict, m_sources)
            Graphs.means_labels(self.exl_dict, m_sources)
            Graphs.inception(self.means, means2)
            self.bar_graph_2(x_axis, y_axis, self.columns[0], zip(m_sources, means2))
        else:
            self.bar_graph_1(x_axis, y_axis, self.columns[0])

    def axis_and_line_graph(self):
        '''This is for the line graph functions'''
        labels = []
        m_labels = []
        Graphs.inception(self.x_prep, labels)
        if self.line_mean_box.isChecked():
            Graphs.means_labels(self.sql_dict, m_labels)
            Graphs.means_labels(self.exl_dict, m_labels)
            self.line_graph_2(self.columns, zip(labels, self.y_prep), zip(m_labels, self.means))
        else:
            self.line_graph_1(self.columns, zip(labels, self.y_prep))

    def axis_and_pie_graph(self):
        '''This is for the pie chart function'''
        titles = []
        Graphs.inception(self.x_prep, titles)
        self.pie_graph(zip(titles, self.y_prep))

    def cols(self):
        '''Inserts items from the column_view list widget into the self.columns list, for the backend graph functions'''
        self.columns.clear()
        Graphs.cols(self.column_view_t1, self.columns)

    def bar_graph_final(self):
        '''For the 'Bar Graph' button'''
        self.cols()
        if len(self.columns) == 0:
            self.err_t1.setText("Select a measurable")
        elif len(self.columns) == 1:
            self.sql_bar_graph()
            self.exl_bar_graph()
            self.sql_means()
            self.exl_means()
            self.axis_and_bar_graph()
            self.clear_house()
        else:
            self.err_t1.setText("This feature only supports one measurable")

    def line_graph_final(self):
        '''For the 'Line Graph' button'''
        self.cols()
        if len(self.columns) < 2:
            self.err_t1.setText("Need more than one measureable")
        else:
            self.sql_lp_graph()
            self.exl_lp_graph()
            self.sql_means()
            self.exl_means()
            self.axis_and_line_graph()
            self.clear_house()

    def pie_chart_final(self):
        '''For the 'Pie Chart' button'''
        self.cols()
        if len(self.columns) < 2:
            self.err_t1.setText("Need more than one measureable")
        else:
            self.sql_lp_graph()
            self.exl_lp_graph()
            self.axis_and_pie_graph()
            self.clear_house()

########################TAB 2#########################

###Conversion functions###

    def search_file(self):
        '''Searches for .xlsx files'''
        self.err_t2.setText("")
        path = QFileDialog.getOpenFileName(self, 'Open XLSX', os.getenv('HOME'), 'XLSX(*.xlsx)')
        self.path.setText(str(path).replace("(", "").replace(")", "").replace(", 'XLSX*.xlsx'", "").replace("'", ""))
        #the line above makes the path readable for the program

    def save_path(self):
        '''Saves the .xlsx path in the excel_paths SQLite table'''
        try:
            path = self.path.text()
            if ".xlsx" not in path:
                raise ValueError
            with conn:
                c.execute("INSERT INTO excel_paths(path) VALUES(?)", (path,))
            self.exl_options()
        except ValueError:
            self.err_t2.setText("Invalid path")

    def exl_to_sql(self):
        '''For the conversion button'''
        try:
            self.err_t2.setText("")
            self.pandas_conversion(self.path.text())
            self.sql_options() #refills sql_source_t2
            self.other_windows(Naming_Tables()) #opens a popup menu recommending that you change the name of the newly created table
        except FileNotFoundError:
            self.err_t2.setText("File not found")

    def pandas_conversion(self, path):
        '''This converts Excel files to SQlite tables'''
        wb = pd.ExcelFile(path)
        for sheet in wb.sheet_names:
            df = pd.read_excel(path,sheet_name=sheet)
            df.to_sql(sheet, conn, index=False, if_exists="replace")

###Excel file setup###

    def exl_options(self):
        '''Fills the Excel file menu with stored paths from the excel paths SQLite table'''
        self.exl_source_t2.clear()
        SQL.menu_add("path", "excel_paths", self.exl_source_t2)

    def upload_exl_1(self):
        '''Sets up the structure of the student_info_table and stores the path to the selected excel file'''
        try:
            self.err_t2.setText("")
            path = self.path.text()
            self.save_path()
            self.upload_btn_menus(path)
            self.path.clear()
            self.notices("exl") #so the user knows the program is working with an excel file, rather than an SQLite database
        except FileNotFoundError: #in case the path does not work
            self.err_t2.setText("Needs to be a '.xlsx' file")
            self.path.clear() #clears the lineedit widget. even when an error is made

    def upload_exl_2(self):
        '''This is for the Use File button in the middle of the page, using the excel path from the excel paths SQLite table'''
        self.err_t2.setText("")
        self.student_menu_t2.clear()
        self.column_menu_t2.clear()
        source = self.exl_source_t2.currentText()
        self.sources_t2.append(source)
        Excel.menu_add(source, "Students", self.student_menu_t2)
        self.column_menu_t2.addItem("Choose all...")
        Excel.menu_add_cols(source, "Students", self.column_menu_t2)
        self.notices("exl")

    def upload_btn_menus(self, path):
        '''Extracts data for the student and column menus, depending on which excel path is being used'''
        self.student_menu_t2.clear()
        self.column_menu_t2.clear()
        self.sources_t2.append(path)
        self.column_menu_t2.addItem("Choose all...")
        Excel.menu_add_cols(path, 'Students', self.column_menu_t2)
        Excel.menu_add(path, 'Students', self.student_menu_t2)

    def exl_table(self, path, name): #backend for extracting data for the table, using data from Excel files
        try:
            headers = []
            data = [name]
            workbook = xlrd.open_workbook(path)
            sheet = workbook.sheet_by_index(0)
            Excel.list_add_cols(path, headers)
            students = Excel.data_list(sheet, 0)
            inx = students.index(name)
            for column in self.columns_t2:
                inx2 = headers.index(column)
                grades = Excel.data_list(sheet, inx2)
                data.append(grades[inx])
            self.table_cols_headers() #setup for the table structure
            self.exl_tabledata(data) #inserts data into the table structure
        except ValueError:
            pass
        except IndexError:
            pass

    def exl_tabledata(self, data): #data parameter must be a list
        '''Inserts data into the table structure'''
        for row_number, row_data in enumerate(data):
            for column_number, column_data in enumerate(str(row_data)):
                self.student_info_table.setItem(column_number, row_number, QtWidgets.QTableWidgetItem(str(row_data)))

###SQLite table setup###

    def upload_sql(self):
        '''Uploads a SQLite table chosen by the user'''
        self.err_t2.setText("")
        source = self.sql_source_t2.currentText()
        self.sources_t2.append(source)
        self.sql_students_t2(source)
        self.sql_columns_t2(source)
        self.notices("sql") #so the user knows the program is working with an SQLite database, rather than an excel file

    def sql_students_t2(self, source):
        self.student_menu_t2.clear()
        SQL.menu_add("Students", source, self.student_menu_t2)

    def sql_columns_t2(self, source):
        self.column_menu_t2.clear()
        self.column_menu_t2.addItem("Choose all...")
        SQL.menu_add_cols(source, self.column_menu_t2)

    def sql_table(self, source, name):
        '''Completes the table function using data from a SQLite table'''
        self.table_cols_headers() #sets up the table structure
        students = []
        SQL.list_add("Students", source, students)
        index = students.index(name) + 1
        self.sql_tabledata(source, index)

    def sql_tabledata(self, source, inx):
        '''Inserts data into the table strucutre, using data from a SQLite table'''
        self.student_info_table.setRowCount(0)
        database = c.execute('SELECT * FROM {} WHERE rowid = {}'.format(source, inx))
        for row_number, row_data in enumerate(database):
            self.student_info_table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.student_info_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

    def sql_options(self):
        '''Fills the sql menu'''
        self.sql_source_t2.clear()
        SQL.tables_info(self.sql_source_t2)

####Main Table Functions####

    def table_cols_headers(self):
        '''Sets up the strucutre of the table'''
        headers = self.columns_t2
        headers.insert(0, "Student")
        self.student_info_table.setColumnCount(len(headers))
        self.student_info_table.setHorizontalHeaderLabels(headers)
        self.student_info_table.setRowCount(1)

    def all_cols(self):
        '''When the user selects 'Choose all...', all columns from the column menu appear in the list widget'''
        cols = [self.column_menu_t2.itemText(i) for i in range(self.column_menu_t2.count())]
        cols.remove("Choose all...")
        for c in cols:
            self.column_view_t2.addItem(c)


    def add_column_t2(self):
        '''Adds columns to the list widget in Tab 2'''
        try:
            self.err_t2.setText("")
            column = self.column_menu_t2.currentText()
            if column == "":
                raise ValueError
            elif column == "Choose all...":
                self.all_cols()
                self.column_view_t2.setCurrentRow(0)
            else:
                self.column_view_t2.addItem(column)
                self.column_view_t2.setCurrentRow(0)
        except ValueError:
            self.err_t2.setText("Menu is empty")

    def remove_column_t2(self):
        '''Removes columns from the list widget'''
        self.err_t2.setText("")
        selected = self.column_view_t2.currentRow()
        self.column_view_t2.takeItem(selected)

    def show_info(self):
        '''Activates the table functions for SQLite tables or Excel files'''
        try:
            self.err_t2.setText("")
            Graphs.cols(self.column_view_t2, self.columns_t2)
            source = self.sources_t2[-1]
            name = self.student_menu_t2.currentText()
            if ".xlsx" in source:
                self.exl_table(source, name)
            else:
                self.sql_table(source, name)
            self.columns_t2.clear()
        except IndexError:
            self.err_t2.setText("Choose SQLite or Excel file")

    def clear_table(self):
        '''Clears table info'''
        self.err_t2.setText("")
        self.columns_t2.clear()
        self.student_info_table.setRowCount(0)
        self.student_info_table.setRowCount(1)

    def notices(self, key):
        '''Allows the user to know if an Excel file is uploaded for usage or a SQLite table is uploaded'''
        if key == "sql":
            self.sql_notice.setText("***")
            self.exl_notice.setText("")
        elif key == "exl":
            self.sql_notice.setText("")
            self.exl_notice.setText("***")


if __name__ == "__main__": #this program is activited only when the name of the file is called
    import sys
    conn = sqlite3.connect('SA.db')
    c = conn.cursor()
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
    c.close()
    conn.close()
