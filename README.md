# WebNote

#### Video Demo: https://youtu.be/FOVf_6zC3Mk
#### Description:
## Introduction
It is a web based application. Using this application, user can create his own account using username and password. User can write notes and save, edit and delete it. This web application is constructed using Flask framework. For frontend, I have used HTML, CSS, JavaScript and bootstrap. For backend, python programming language is used and sqlite3 is used for database.
Project directory includes app.py, helper.py, requirements.txt, templates, static and flask_session. app.py file is typically serves as the main entry point for Flask application. It contains the configuration, routes, and logic for handling HTTP requests and rendering web pages. In this file, sql database is configured through the sqlite3.
## Specification
### Register
It is implemented in such a way that user can register for an account via a form which requires username and password. If the fields in form are blank or username already exist or not obey the password conditions, it won't allow to submit the form and show appropriate commands to the user. user's input get submitted via post method. Internally, hash of the password and username were inserted into the database. If user register successfully, then user redirected to the index page.
### Index
It includes a form which contain text type input for heading of the note and a textarea for writing notes and a submit button. It needs some conditions to be true to submit the form that are heading and notes should not be blank, heading can have atmost 200 characters, number of words in notes limited to 500 words. Using the javascript, number of words in the textarea is calculated and make the user unable to type after reaching 500 words. When form get submitted, user inputs and date and time is stored in notes table in database. Date and time is stored as julianday type. Thereby, we can store date and time in single column. Let's discuss the structure of the database in upcoming paragraph.
### view
It include all the saved forms from index page and search box to search the notes based on the heading of the notes. Each saved form has three buttons. They are edit button, update button and delete button. Edit button let the user to edit the notes and heading.
+ Update button is used to save the editted form. It only activated after edit button is clicked. When update button is clicked, the particular form is submitted via post method. Based on the notes id and user id, notes get updated in database via UPDATE command.
- Delete can be used to delete the notes. When user clicks delete button, browser ask for the confirmation to the user. This technique prevent accident click of delete button. The function associated with the edit and delete button were constructed using the javascript. When delete button clicked and confirmed by user, the particular form is submitted via poat method. Based on the noted id and user id, notes get deleted from the database via DELETE command.
### login
It include a form which contain username and password fields. If username or password field is empty or misspelled, appropriate message is displayed to the user. If user and password match correctly, then user will redirect to the index page.
### logout
When user logged in, user can see logout button in right corner. When logout button is clicked, flask session of the page are cleared and user will redirect to login page.
### layout
Layout is a base template which defines the common structure of the website. In this page, headline of the page and nav bar were implemented. Thereby, these things are commonly shred with all pages. The purpose of a layout template is to provide a consistent look and making it easier to maintain and update the overall design.
### Database
Sqlite3 database is used to manage the database. Database is created on name webnote.db. This db has two tables. One is users which has three fields id, username and password. id is primary key and username is unique key so it won't allow duplicates. Other one is notes which has notes id, user id, heading and notes. notes id is primary key and user id is foreign key.
### helper
It is python file where functions were defined so that those function can be imported into the app python file. It has function definition for login_required (it ensure user has logged in), checkValidPass (it check some condition for password), remember_login (it save user id in session), get_db_connection (it is used to connect with database), getJulianday (It is used to get julianday of current time).
## Conclusion
This notes taking web based application allow the user to take notes at anywhere and anytime. Notes written by the user can be protected and can be used in future. By building this application, I got familiarize with Flask framework , python, HTML, CSS, JavaScript, bootstrap and sql commands. Thank you David Malan and CS50 team for this good opportunity to explore computer science.


# Framwork: Flask
# Frontend: HTML, CSS, JavaScript and Bootstrap
# Backend: Python
# Database: Sqlite3
