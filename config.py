class Config(object):
    DEBUG = False
    CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tasks'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    BUNDLE_ERRORS = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    BUNDLE_ERRORS = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}