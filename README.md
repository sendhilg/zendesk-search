# Zendesk Search

## Description
The application is completed as a task following the [brief](BRIEF.md).

## Requirements
The application was developed using python version 3.7.3 on a windows 10 machine 
using Visual Studio Code for coding and GitBash for running commands.

To check the version on your machine run the below command:

    $ python --version

## Cloning the project and running the application

Clone the project from github.

    $ git clone https://github.com/sendhilg/zendesk-search.git

Change into the project directory 'zendesk-search'.

    $ cd zendesk-search

Setup a virtual environment.

    On windows (GitBash Terminal):

        $ pip install virtualenv
        $ python -m venv zendesk_venv
        $ source ./zendesk_venv/Scripts/activate
    
    To verify that the virtualenv is activated, run the below command and 
    check that the package source is the vitualenv i.e 'zendek_venv':

        $ pip -V

    On Linux systems (Bash Terminal):

        $ pip install --user virtualenv
        $ python -m venv zendesk_venv
        $ source ./zendesk_venv/bin/activate
