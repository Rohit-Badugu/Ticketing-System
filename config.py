class Config(object):
    DEBUG = False
    TESTING = False

    #Base 64 encoded API KEY
    API_KEY = "Basic cmJhZHVndUBhc3UuZWR1L3Rva2VuOmRIR1YzbHYxbzRlSHlGNnJtR2NmZVF0UmNxaXJxZDN4MXhDWGtHMU0="
    
    #Specifies how many tickets must be shown in a page
    num_tickets_in_page = 25

    #Zendesk ticket host
    host = "https://zccrbadugu.zendesk.com/"

    #List of Endpoints
    api_tickets = "/api/v2/tickets"
    api_single_ticket = "api/v2/tickets/{}"
    api_multiple_users = "api/v2/users/show_many"
    api_groups = "api/v2/groups"
    api_comments = "api/v2/tickets/{}/comments"

#Config for Production Server
class ProductionConfig(Config):
    pass

#Config for Development Server
class DevelopmentConfig(Config):
    DEBUG = True

#Config for Test Server
class TestingConfig(Config):
    TESTING = True
