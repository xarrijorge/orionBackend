from .. import app  # Import the app instance
import psycopg2
import click


# Connect to the database using app configuration
def get_db():
    conn = psycopg2.connect(
        dbname=app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1],
        user=app.config['SQLALCHEMY_DATABASE_URI'].split('://')[1].split(':')[0],
        password=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[2].split('@')[0],
        host=app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1].split(':')[0],
        port=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[3].split('/')[0]
    )
    return conn


def init_db():
    db = get_db()


def close_db(e=None):
    db = get_db()
    db.close()



@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)