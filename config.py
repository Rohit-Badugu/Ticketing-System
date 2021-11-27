class Config(object):
    DEBUG = False
    TESTING = False
    API_KEY = "Basic cmJhZHVndUBhc3UuZWR1L3Rva2VuOmRIR1YzbHYxbzRlSHlGNnJtR2NmZVF0UmNxaXJxZDN4MXhDWGtHMU0="
    num_tickets_in_page = 25

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
