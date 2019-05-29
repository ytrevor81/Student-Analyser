# Student-Analyser
A desktop app to analyze and evaluate students in all of your classes!

<h1>Technologies:</h1>
Python 3 - PyQt5 - Matplotlib - SQLite3 - xlrd (for Excel files) - Pandas - Numpy

<h1>Tab 1:</h1>
This is the analysis section of the app. You can upload as many SQLite tables and .xlsx files as you want, as long as the Excel paths are stored in the SA.db file (you can store the paths in Tab 2). You can analyze students and their grades using three data visualization tools: you can utilize bar graphs, line graphs, and pie charts, depending on what you want to analyze. You also have the option to visualize the mean of the grades/scores you are analyzing and compare it to the grades of individual students.


![tab_1](https://user-images.githubusercontent.com/46886041/56731699-57a12280-6785-11e9-814a-59619ff17e0a.PNG)

<h1>Tab 2</h1>
This is the students section of the app. You can search for .xlsx files, upload them into the app for usage and/or convert the file into a SQLite table. You can also view your students' grades using the table widget. This works for both Excel files and SQLite tables.


![tab_2](https://user-images.githubusercontent.com/46886041/56731723-64257b00-6785-11e9-9b1c-3b34b60f0ef3.PNG)

<h1>Grading:</h1>
When you click the "Custom Rubrics/Grading" button, this pop-up window will appear. You can create and store your own grading rubrics, upload any rubrics you created in the past, grade students using a specialized calculator (utilizing the particular rubric you chose) and insert their scores. You can insert their grades directly into the SQLite table in which their information is stored. 


![grading](https://user-images.githubusercontent.com/46886041/56731382-8a96e680-6784-11e9-916c-f5658d38f108.PNG)

