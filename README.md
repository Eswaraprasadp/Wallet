# Wallet
## Description
Add expenses, and modify them
## Installation and Usage
Open Command Prompt and Change the directory to the cloned repository.
Create a virtual environment (venv) in Python. Then, 
For Windows, run the following commands
```
$ venv\Scripts\activate
$ (venv) flask run
``` 
For Linux, Mac and other Operating Systems, run the following commands
```
$ venv/Scripts/activate
$ (venv) flask run
``` 
Then, visit
```
http://127.0.0.1:5000/
```
or
```
localhost:5000
```
on your browser to navigate to the site

> **Note:** If exceptions about db are thrown, delete the migrations folder and run the following commands:
 ```
$ (venv) flask db init
$ (venv) flask db migrate
$ (venv) flask db upgrade
```
