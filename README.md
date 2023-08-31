# BoilerPlate Fast API Microservice

This is a FastAPI microservice boilerplate. Which has the following features:


## Technologies used:

- FastAPI
- Uvicorn
- Docker
- Docker Compose
- Make
- Python
- Database (Postgres)

## Folder Structure

We have the following folder structure, inspired by [Netflix Dispatch Project](https://github.com/Netflix/dispatch/tree/master) and [Boiler Plate from Github](https://github.com/teamhide/fastapi-boilerplate):

```bash
.
├── migrations                  # Database migrations folder
├── scripts                     # Scripts folder
│   ├── deployment              # Deployment scripts folder which contains scripts for deployment
├── tests                       # Tests folder
├── requirements                # Requirements folder
├── .dockerignore               # Dockerignore file for the application
├── .env                        # Environment variables for the application
├── .gitignore                  # Gitignore file for the application
├── Dockerfile                  # Dockerfile for the application
|── docker-compose.yml          # Docker compose file for the application to start local instance as dev
├── Makefile                    # Makefile for the application
├── README.md                   # README file
├── src                         # Application Source folder
│   ├── __init__.py             # Init file for the application 
│   ├── routes.py               # Central routes file for the application. Also contains the health check route
│   ├── main.py                 # Init file for the application
│   ├── <modules>               # Modules folder for the application where we define the feature details of the microservice
├── core                    # Core folder for the application
│   ├── __init__.py         # Init file 
│   ├── config.py           # Config file for the application
│   ├── decorators.py       # Decorators file for the application
│   ├── logging.py          # Logging setup file for the application
│   ├── database.py         # Database file for the application
│   ├── dependencies.py     # Dependencies file where certain validation and checks can be defined
│   ├── models              # Core Models Folder for the application
│   │   ├── __init__.py     # Init file for the models
│   │   ├── base.py         # Base file for the models, where we define base models and mixins
│   │   ├── enums.py        # Core Enums
│   ├── exceptions          # Exceptions folder for the application
│   │   ├── __init__.py     # Init file for the exceptions
│   │   ├── base.py         # base Exceptions file for the application
│   ├── security.py         # Security file for the application
│   ├── utils               # Utils folder for the application
│   │  ├── __init__.py      # Init file 
│   │  ├── pagination.py    # Database file for the application

```

Each module will have following files:

1. `routes.py` - This file will contain the routes for the module, calls the services and returns the response
2. `services.py` - This file will contain the services for the module - treat this as a controller
3. `models.py` - This file will contain the models for the module
4. `schemas.py` - This file will contain the schemas for the module - `pydantic` models
5. `__init__.py` - This file will contain the init file for the module
6. Additional files for the module, not mandatory but required for modular code
    1. `enums.py` - This file will contain the enums for the module
    2. `dependencies.py` - This file will contain the dependencies for the module like validators
    3. `utils.py` - This file will contain the utils for the module
    4. `exceptions.py` - This file will contain the exceptions for the module

> This follows Model, Schema, Service, Route pattern. Note: we are assuming that the module or micro service doesn't have any UI rendering and is only an API service.

## Description

This is a boilerplate for a FastAPI microservice. It includes a Dockerfile, a docker-compose file, a Makefile, and a .gitignore file.

## Installation

```bash
$ git clone
$ cd
$ make build
$ make run
```

## Usage

```bash
$ curl -X GET http://localhost:8000
```

## License

[MIT](https://choosealicense.com/licenses/mit/)



## References

Some other places where the folder structure is inspired from:
1. https://betterprogramming.pub/fastapi-best-practices-1f0deeba4fce
2. https://bitestreams.com/blog/fastapi_sqlalchemy/
3. https://alembic.sqlalchemy.org/en/latest/tutorial.html?source=post_page-----5c53d3880f12--------------------------------#the-migration-environment
4. In future we can avoid schema and model definition to be different using this: https://github.com/tiangolo/sqlmodel
5. Postgres Async connection: https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg
6. Poetry commands: https://python-poetry.org/docs/cli/
7. https://testdriven.io/blog/fastapi-docker-traefik/
8. understanding the SQLAlchemy session strategy: https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session
   1. https://dev.to/behainguyen/python-sqlalchemy-understanding-sessions-and-associated-queries-12a7
   2. 



---

## Setup of project Base

### 1. Create a new project directory

Based on the above recommendations, we will create a new project directory as per the project name. Ensure you have the corresponding repository created and link the directory based on the instructions provided by Github.


### 2. Docker Compose File

We will simulate the production environment locally using Docker Compose. We will create a docker-compose.yml file in the root of the project directory. This file will contain the following:

1. Database - Postgres
2. Application - FastAPI

Rememeber the Postgres database is only for development purposes. For production, we will use a managed database service like AWS RDS. And this file ensures there is a DB instance running locally for development purposes.

> We need to ensure these variables are set in the .env file as well.

Also, note that our Application is running on port 8013 and docker is asked to expose this. The default port for FastAPI is 8000 but we have changes it for our usecase. We changed this port in the .env file as well.

To invoke the application start we point to Docker File which we will create in the next step.

Learnings

Local Docker + Postgres Setup:

1. When we add port in the docker compose file it is for us to connect on different port for our DB client of choice
   1. For the docker compose orchestration we can still use the 5432 port to connect to the DB as the host will the one specificed in the compose file.
2. This means that the DB host and port for our dockerized application is not a local one but the one specified in the compose file.

### 3. Docker File

We will create a Dockerfile in the root of the project directory. This file will contain the following:

1. Basic code setup
2. Install dependencies using Poetry
   1. We need to ensure that we have the pyproject.toml and poetry.lock files in the root of the project directory
   2. We also need to update to the latest version of Poetry
3. Expose port
4. Start the application
5. Setup Health Check endpoint - useful for ECS deployments

> Note: we are not using "FROM tiangolo/uvicorn-gunicorn-fastapi:python3.*" base image. As this supports different folder structure which has nested app folder.


### 4. Makefile

We will create a Makefile in the root of the project directory. This file will contain the following:

1. Build the application
2. Run the application
3. Run the application in development mode
4. Run the application in production mode
5. Run the application in test mode


### 5. Application Configurations


First, we will create a config.py file in the core folder of the project directory. This file will contain base configurations driven from environement files. Then we will define the logging and database configurations in the logging.py and database.py files respectively. These files will be in the core folder of the project directory.

Rememeber we create the constructs of the classes but instantiate them in the main.py file.


### 6. Alembic Setup

Read the below resources, after the new model is defined it is mandatory to place them in the env.py file under the alembic folder. This is required for the migration to work.

1. https://ahmed-nafies.medium.com/fastapi-with-sqlalchemy-postgresql-and-alembic-and-of-course-docker-f2b7411ee396
2. https://alembic.sqlalchemy.org/en/latest/tutorial.html?source=post_page-----5c53d3880f12--------------------------------#the-migration-environment



### 7. Database Setup

We have basic session setup to support async database connections. But currently we will support on sync - the most common way for SQLAlchemy connection. 

Also, with in the scope of the SQLAlchemy we are using the scoped session strategy. Read more about it here: https://dev.to/behainguyen/python-sqlalchemy-understanding-sessions-and-associated-queries-12a7

More detailed reading can come from main documentation of SQLAlchemy and exploring open source projects.

### 8. Dependency Management

We will use Poetry for dependency management. We will create a pyproject.toml file in the root of the project directory. This file will contain the following:

1. Project name
2. Project version & other details
3. Base dependencies
4. Dev dependencies
5. Test dependencies

There are other layers but we will add them as per our reqirements for the future.

Read about the Poetry commands here: https://python-poetry.org/docs/cli/

Main thing to rememeber are the following commands:

1. poetry add <package_name> - installs the package and adds it to the pyproject.toml file
2. poetry install - installs all the dependencies
3. poetry lock - locks the dependencies. This is important for the docker build process. As it will install the dependencies from the lock file and not the pyproject.toml file.
4. poetry update - updates the dependencies
5. poetry remove <package_name> - removes the package and updates the pyproject.toml file
6. poetry show - shows the dependencies
