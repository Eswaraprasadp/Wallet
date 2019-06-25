# Wallet
## Description
Add expenses, and modify them
## Installation and Usage
Open Command Prompt and Change the directory to the cloned repository.
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

> **Note:** If exceptions about db are thrown, delete the migrations folder and run the following commands:
 ```
$ (venv) flask db init
$ (venv) flask db migrate
$ (venv) flask db upgrade
```
