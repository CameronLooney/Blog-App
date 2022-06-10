import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # set key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sdfvcdfgvbgfdswedfgvbnhg'
    # url for sql db will either be given or else if not place it in the current directory
    # taking the database URL from the DATABASE_URL environment variable, and if that isn’t defined,
    # config app.db located in the main directory of the application, which is stored in the basedir variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['cameronlooney18@gmail.com']
    POSTS_PER_PAGE = 20

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
