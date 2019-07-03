# Zendesk Search

## Description
The application is completed as a task following the [brief](BRIEF.md).


## Requirements
The application was developed using python version 3.7.3 on a windows 10 machine 
using Visual Studio Code for coding and GitBash for running commands.

To check the version on your machine run the below command:

    $ python --version


## Cloning the project and setting up the environment:
Clone the project from github:

    $ git clone https://github.com/sendhilg/zendesk-search.git


Change into the project directory 'zendesk-search':

    $ cd zendesk-search


Setup a virtual environment for the application using virtualenv tool:

    virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that a Python application would need.

    On windows (GitBash Terminal):

        $ pip install virtualenv
        $ python -m venv zendesk_venv
        $ source ./zendesk_venv/Scripts/activate

    On Linux systems (Bash Terminal):

        $ pip install --user virtualenv
        $ python -m venv zendesk_venv
        $ source ./zendesk_venv/bin/activate

    To verify that the virtual environment is activated, run the below command and 
    check that the source for pip (python package manager) is the vitual environment i.e 'zendek_venv':

        $ pip -V

After the virtual environment is created, use the package manager 'pip' to install 
requirements for the application.

    $ pip install -r requirements.txt


## Creating tables and loading data for search:
The project uses [Django](https://www.djangoproject.com/) framework to create table in a default SQLite Database. Django ORM is used to load data from json files.

    Create tables by running the migrate command at the project directory:

        $ python manage.py migrate

    Place the files(organizations.json, users.json, tickets.json) in the project directory 
    and load data for search using the django management command:

        $ python manage.py load_data


## Searching data:
After the data is loaded successfully by using the load_data command, run the below django 
management command at the project directory to search for data:

    $ python manage.py search

The search supports below:
1. Full matching search
1. Case insensitive search (E.g. searching for 'megacorp' will display both 'megacorp' and 'Megacorp')
2. Substring search (E.g. searching for 'mega' will display 'mega', 'megacorp' and 'Megacorp')


### Example
```
$ python manage.py search

Welcome to Zendesk Search

Select from the below options. Type 'quit' to exit the application, 'menu' to display the main menu at any time.

Search options:
        * Enter 1 to search Zendesk.
        * Enter 2 to view a list of searchable fields.
        * Enter 'quit' to exit application.
        * Enter 'menu' to display menu.

Enter your choice:
1

Select 1) Users or 2) Tickets or 3) Organizations
3

Enter search term:
_id

Enter search value:
112

Searching organizations for _id with a value of 112

_id                           112
url                           http://initech.zendesk.com/api/v2/organizations/112.json
external_id                   32e979ff-47b4-43b9-8b74-eea1227905d9
name                          Quilk
domain_names                  ['valreda.com', 'strozen.com', 'signity.com', 'quantasis.com']
created_at                    2016-01-10T03:21:25 -11:00
details                       MegaCorp
shared_tickets                False
tags                          ['Hall', 'Dorsey', 'Shepard', 'Carter']
user_id                       28
user_name                     Terri Mcmahon
ticket_id                     0533df4e-488f-45dd-b4b8-e238be0690ed
ticket_subject                A Drama in Bulgaria

```

## Unit Tests

### Running unit tests
Run the below commands at the project directory to run tests with code coverage.

    $  pytest --cov=search --cov-report=term --cov-report=html --cov-fail-under=75 --no-cov-on-fail --junitxml=unittest-report/xml/results.xml
