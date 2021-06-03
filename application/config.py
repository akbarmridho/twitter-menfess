from os import environ


class Config:
    FLASK_DEBUG = True
    DEVELOPMENT = True
    FLASK_ENV = 'development'
    APP_KEY = environ.get('APP_KEY')


class ProductionConfig(Config):
    FLASK_DEBUG = False
    DEVELOPMENT = False
    FLASK_ENV = 'production'


def get_config() -> Config:
    mode = environ.get('APP_ENV')
    if mode == 'production':
        return ProductionConfig()
    else:
        return Config()
