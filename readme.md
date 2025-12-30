# TODO APP Brief Introduction

# Use the following commands to test and run the todo app
### Install libraries: 'pip install -r requirements.txt'
### Test App: 'python -m pytest'
### Run App: 'python -m todo_app.app'

# Project structure
### todo_app
### --- todo_app
### --- --- __init__.py
### --- --- app.py
### --- --- database.py
### --- --- static/
### --- --- templates/
### --- --- --- index.html
### --- --- --- add_task.html
### --- --- css/
### --- --- --- style.css
### --- --- js/
### --- --- --- app.js
### --- tests
### --- --- __init__.py
### --- --- test_app.py
### --- --- conftest.py

## Brief Intro of Each File:
### app.py, the main flask app server and api logics responsible for crud operations
### database.py, the database file responsible for creating a database for todo app.
### index.html, a web dashboard
### add_task.html, webbased form which accepts user inputs
### style.css, webpage stylesheet
### app.js, responsible for javascript operations likes create, update, delete and load task
### test_app.py, responsible for testing todo_app
### conftest.py, it defines a pytest fixture that creates a temporary database and test client for isolated, reusable testing of your Flask app.

# A Live Demo is included. 

<video width="640" height="360" controls>
  <source src="https://drive.google.com/file/d/19z5oKpMHbeNG695NkcGAXsr1vMMEGtcR/view" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Link: https://drive.google.com/file/d/19z5oKpMHbeNG695NkcGAXsr1vMMEGtcR/view?usp=sharing



