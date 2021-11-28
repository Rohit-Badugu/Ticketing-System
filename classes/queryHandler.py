from classes.client import ApiClient
from classes.utils import Utils
from config import Config

class QueryHandler:
    def __init__(self):
        self.apiClient = ApiClient.getInstance()
        self.utils = Utils()
        self.config = Config()

    #Fetches multiples tickets using offset pagination.
    def fetchTickets(self, page_no):
        return self.apiClient.getTickets(self.config.api_tickets, page_no)

    #Fetches single ticket
    def fetchSingleTicket(self, ticket_id):
        return self.apiClient.getSingleTicket(self.config.api_single_ticket.format(ticket_id))

    #Fetches multiple users by passing comma seperated userIDs in url params
    def fetchMultipleUsers(self, tickets):
        userIDs = self.utils.getUserIDs(tickets)
        return self.apiClient.getMultipleUsers(self.config.api_multiple_users, userIDs)

    #Fetches all the groups in the system
    def fetchGroups(self): 
        return self.apiClient.getGroups(self.config.api_groups)

    #Fetches the comments for a specific ticket
    def fetchComments(self, ticket_id):
        return self.apiClient.getComments(self.config.api_comments.format(ticket_id))
        
    def fetchTicketUsers(self, ticket, comments):
        userIDs = self.utils.getTicketUserIDs(ticket, comments)
        return self.apiClient.getMultipleUsers(self.config.api_multiple_users, userIDs)