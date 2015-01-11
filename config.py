import os

# For WTF-Forms
WTF_CSRF_ENABLED = True
SECRET_KEY = '1121wsefjefepfooffiKFFPWDWMNCkY^%$&##))#*E(#(#'

# For SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')