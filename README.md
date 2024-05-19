# Delusion

Telco network topology tool for the nodes' visualization, as well as connections between them.

## Table of contents

* [Stack](#stack)
* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Endpoints](#endpoints)
* [Pre-commit hook](#pre-commit-hook)

## Stack

* Framework: Django + Django REST Framework
* Formatters: Black + Isort
* Linters: Flake8, Pylint
* Build tools: Pyenv
* Type checking: Mypy
* Security check: Bandit
* Documentation: Drf-spectacular
* Containerization: Docker

## Prerequisites

This project can be run through Docker and local machine. For running through Docker, all you need is Docker. Otherwise, your machine needs to have Python (v 3.9), Python and PostgreSQL(v 14.5) installed.

## Setup

Description of how to set up the project to be able to start the development.

### If using docker

Before running these, make sure you have created `.env` files in dirs where `.env.example` is present and include all required variables there.

    # Build the project.
    $ docker compose build

    # Start the project.
    $ docker compose up -d

    # Stop the project.
    $ docker compose down

### If running without docker

Before running these make sure to create `.env` file in base directory with all required variables. See `.env.example` file

    # Install dependencies.
    $ pip install -r requirements.txt

    # Start the project.
    $ python manage.py runserver

you also need to make sure that postgres is installed and running on your machine

## Endpoints

Endpoints can be viewed at swagger and redoc. They will be available after project has been successfully set up and running.

* Swagger: /api/schema/swagger-ui/
* Redoc: /api/schema/redoc/


## Pre-commit hook

This project has pre-commit hook which is used to run checking before each commit. It prevents developers from making commits that have bad formatting or errors. It needs to be set up with following commands

    # Set up git hook.
    $ poetry run pre-commit install

    # Run pre-commit hooks.
    $ poetry run pre-commit run
#
