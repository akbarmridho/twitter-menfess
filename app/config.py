from os import environ


class Config:
    DEBUG = True
    DEVELOPMENT = True
    ENV = 'development'
    APP_KEY = environ.get('APP_KEY')


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    ENV = 'production'


def get_config() -> Config:
    mode = environ.get('APP_ENV')
    if mode == 'production':
        return ProductionConfig()
    else:
        return Config()
