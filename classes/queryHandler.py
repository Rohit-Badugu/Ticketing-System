from classes.client import ApiClient
from classes.utils import Utils

class QueryHandler:
    def __init__(self):
        self.apiClient = ApiClient.getInstance()
        self.utils = Utils()

    def fetchTickets(self, page_no):
        api_endpoint = "/api/v2/tickets"
        return self.apiClient.getTickets(api_endpoint, page_no)

    def fetchTicketInfo(self, ticket_id):
        api_endpoint = "/api/v2/tickets/" + ticket_id
        return self.apiClient.getTicketInfo(api_endpoint)

    def fetchUserInfo(self, tickets):
        userIDs = self.utils.getUserIDs(tickets)
        api_endpoint = "api/v2/users/show_many"
        return self.apiClient.getUserInfo(api_endpoint, userIDs)

    def fetchGroups(self): 
        api_endpoint = "api/v2/groups"
        return self.apiClient.getGroups(api_endpoint)

    def fetchComments(self, ticket_id):
        api_endpoint = "api/v2/tickets/" + ticket_id + "/comments"
        return self.apiClient.getComments(api_endpoint)
        
    def fetchTicketUsers(self, ticket, comments):
        userIDs = self.utils.getTicketUserIDs(ticket, comments)
        api_endpoint = "api/v2/users/show_many"
        return self.apiClient.getUserInfo(api_endpoint, userIDs)