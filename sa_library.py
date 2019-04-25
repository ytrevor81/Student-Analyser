import numpy as np
import xlrd
import sqlite3
import math

conn = sqlite3.connect("SA.db")
c = conn.cursor()

class SQL(object):
    '''Reusable methods relating to the SQLite database'''

    @classmethod
    def menu_add(cls, column, table, menu):
        '''Extracts info from a SQLite table and inserts it into a QComboBox widget'''
        l = []
        c.execute("SELECT {} FROM {}".format(column, table))
        for x in c.fetchall():
            l.append(x[0])
        for data in l:
            menu.addItem(data)

    @classmethod
    def menu_add_cols(cls, table, menu):
        '''Extracts column info from a SQLite table and inserts it into a QComboBox widget'''
        l = []
        c.execute("SELECT * FROM {}".format(table))
        for column in c.description:
            l.append(column[0])
        l.remove("Students")
        for column in l:
            menu.addItem(column)

    @classmethod
    def list_add_cols(cls, table, list):
        '''Extracts column info from a SQLite table and inserts it into a list'''
        c.execute('SELECT * FROM {}'.format(table))
        column_names = c.description
        for header in column_names:
            list.append(header[0])

    @classmethod
    def tables_info(cls, menu):
        '''Gathers all SQLite table names from the .db file and inserts them into a QComboBox widget'''
        raw_names = []
        c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        for name in c.fetchall():
            raw_names.append(name)
        shownames = [str(name).replace("(", "").replace(")", "").replace(",", "").replace("'", "") for name in raw_names]
        shownames.remove("rubrics")
        shownames.remove("excel_paths")
        for name in shownames:
            menu.addItem(name)

    @classmethod
    def list_add(cls, column, table, list):
        '''Extracts info from a SQLite table and inserts it into a list'''
        c.execute("SELECT {} FROM {}".format(column, table))
        for x in c.fetchall():
            list.append(x[0])

    @classmethod
    def query_list(cls, column, table, list, inx):
        '''Extracts very specific info from a SQLite table and inserts it into a list'''
        c.execute("SELECT {} FROM {} WHERE rowid = {}".format(column, table, inx))
        for x in c.fetchall():
            list.append(x[0])

    @classmethod
    def readable_list(cls, list):
        '''Makes a list of values, extracted from SQLite, readable for the program and for the user'''
        return [str(i).replace("(", "").replace(")", "").replace(",", "").replace("'", "") for i in list]

    @classmethod
    def readable(cls, input):
        '''Input parameter must be a string from an SQLite database'''
        return input.replace("(", "").replace(")", "").replace(",", "").replace("'", "")


class Excel(object):
    '''Reusable methods relating to .xlsx files'''

    @classmethod
    def data_list(cls, sheet, index):
        '''Makes a list of values from an Excel file'''
        return [sheet.row_values(i)[index] for i in range(sheet.nrows) if sheet.row_values(i)[index]]


    @classmethod
    def menu_add(cls, path, header, menu):
        '''Extracts student info from an Excel file and inserts it into a QComboBox widget'''
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        data = [sheet.row_values(i)[0] for i in range(sheet.nrows) if sheet.row_values(i)[0]]
        data.remove(header)
        for d in data:
            menu.addItem("{}".format(d))

    @classmethod
    def menu_add_cols(cls, path, col, menu):
        '''Extracts column info from an Excel file and inserts it into a QComboBox widget'''
        l = []
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        for header in range(sheet.ncols):
            l.append(sheet.cell_value(0, header))
        l.remove(col)
        for column in l:
            menu.addItem(column)

    @classmethod
    def list_add_cols(cls, path, list):
        '''Extracts column info from an Excel file and inserts it into a list'''
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        for header in range(sheet.ncols):
            list.append(sheet.cell_value(0, header))

class Graphs(object):
    '''These methods are only to help navigate data for graph construction'''

    @classmethod
    def cols(cls, widget, list):
        '''Extracts all columns from a QComboBox widget and inserts them into a list widget'''
        for index in range(widget.count()):
            list.append(widget.item(index).text())

    @classmethod
    def means_labels(cls, dict, list):
        '''Iterates over sources where the 'Include Mean' box has been checked'''
        for source in dict:
            list.append("{} Average".format(source))

    @classmethod
    def inception(cls, list1, list2):
        '''Inserts the values of a nested list into a normal list'''
        for i in list1:
            for ii in i:
                list2.append(ii)
