# flask-dash
A template repo to rapidly build and deploy web apps for data science projects. Built with [Flask](https://github.com/pallets/flask) and [Dash](https://plot.ly/dash/) on a PostgreSQL database, complete with a user login.

## References
This template draws heavily on Miguel Grinberg's [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) and Oleg Komarov's [dash-on-flask](https://github.com/okomarov/dash_on_flask). This template uses a PostgreSQL database instead of an sqlite database file.

## Installation

### Environment

#### Conda & Requirements

We use [conda](https://docs.conda.io/en/latest/miniconda.html) for environment management. Create a new environment:

    conda create -n flashdask python=3.7

Activate your conda environment:

    conda activate flashdask

Clone and change directory into this repo:

    git clone https://github.com/Lkruitwagen/flask-dash.git
    cd flask-dash

Install pip package manager to the environment if it isn't already:

    conda install pip

Install the project packages:

    pip install -r requirements.txt

#### Environment Variables

Save the environment variables we need in activation and deactivation scripts in the conda environment. Follow the [conda instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#setting-environment-variables) for your os, and adapt the following:

    cd $CONDA_PREFIX
    mkdir -p ./etc/conda/activate.d
    mkdir -p ./etc/conda/deactivate.d
    touch ./etc/conda/activate.d/env_vars.sh
    touch ./etc/conda/deactivate.d/env_vars.sh

edit `./etc/conda/activate.d/env_vars.sh` as follows:

    #!/bin/sh
    
    export DATABASE_URL=postgresql://postgres:<YOURPASSWORD>@localhost/flaskdash
    export PYTHONPATH=~/repos/flask-dash
    export FLASK_DEBUG=1
    export FLASK_ENV=development

Leave `<YOURPASSWORD>` blank if you haven't password protected your database (default).

edit `./etc/conda/deactivate.d/env_vars.sh` as follows:

    #!/bin/sh

    unset DATABASE_URL
    unset FLASK_DEBUG
    unset FLASK_ENV

Save and close both files.

### Database

#### PostgreSQL

App data (only user data for now) is stored in a PostgreSQL database. Install PostgreSQL following the generic install instructions for your operating system, e.g. [from Heroku](https://devcenter.heroku.com/articles/heroku-postgresql#set-up-postgres-on-linux).

To set up the database you may first need to change roles to your postgres admin:

    sudo su postgres

Create a database:

    createdb flashdask

#### Migrations

Use Flask migrations to create and manage db migrations. Initialise the database and migrations folder structure:

    flask db init

Create an initial migration:

    flask db migrate -m "Initial migration"

Run the database upgrade:

    flask db upgrade

Beware the limitations of Alembic and manually modify your migrations as appropriate: _In particular, Alembic is currently unable to detect table name changes, column name changes, or anonymously named constraints._

#### Create a user

Individual users can be created using the script in `bin/`:

    bin/create_user.py username username@example.com

You will be prompted to enter a password for that user.

## To Do
- Heroku config