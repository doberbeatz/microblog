import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

TEMPLATES_AUTO_RELOAD = True
CSRF_ENABLED = True
SECRET_KEY = 'secret_key'

# Email server
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_TLS = (os.environ.get('MAIL_USE_TLS') == 'True')
MAIL_USE_SSL = (os.environ.get('MAIL_USE_SSL') == 'True')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# Admins
ADMINS = str(os.environ.get('ADMINS')).split()

# Pagination
POSTS_PER_PAGE = 5
