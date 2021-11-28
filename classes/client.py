import requests, ujson
from requests.exceptions import RequestException
from config import Config

class ApiClient:
    _instance = None    #Singleton class

    def __init__(self):
        if ApiClient._instance != None:
            raise Exception("Cannot instantiate more than one instance of singleton class")
        else:
            ApiClient._instance = self

    '''
    The object of ApiClient is created using getInstance method
    getInstance method returns a reference to singleton object
    '''
    @staticmethod
    def getInstance():
        if ApiClient._instance == None:
            ApiClient()
        return ApiClient._instance

    #Add headers to HTTP requests
    #Authorization header contains the API KEY
    def getHeaders(self):
        headers = {}
        headers["Authorization"] = Config.API_KEY
        headers["Content-type"] = "application/json"

        return headers

    #Makes a HTTP GET call to the api endpoint and returns the json object
    def httpGetJson(self, endpoint, params={}):
        try:
            response = requests.get(Config.host + endpoint, headers=self.getHeaders(), params=params)

            #check the HTTP status code
            status_code = response.status_code
            if status_code == 200:
                #parse the string to form json object
                jsonObject = ujson.loads(response.text)
                return jsonObject
        except RequestException as e:
            #Error occured while fetching data from API endpoints
            print("Request Exception raised")
            print(e.response)

    #Returns all the tickets in the specified page
    def getTickets(self, endpoint, page_no):
        params = {"per_page": Config.num_tickets_in_page, "page": page_no}
        return self.httpGetJson(endpoint, params)
        
    #Returns a single ticket with id = ticketid
    def getSingleTicket(self, endpoint):
        jsonResponse = self.httpGetJson(endpoint)
        if jsonResponse is not None:
            ticket = jsonResponse["ticket"]
            return ticket

    #Returns multiple users
    def getMultipleUsers(self, endpoint, userIDs):
        params = {"ids": userIDs}
        jsonResponse = self.httpGetJson(endpoint, params)
        if jsonResponse is not None:
            userList = jsonResponse["users"]
            return userList

    #Returns all the groups in the system
    def getGroups(self, endpoint):
        jsonResponse = self.httpGetJson(endpoint)
        if jsonResponse is not None:
            groups = jsonResponse["groups"]
            return groups

    #Returns comments for a specific ticket
    def getComments(self, endpoint):
        jsonResponse = self.httpGetJson(endpoint)
        if jsonResponse is not None:
            comments = jsonResponse["comments"]
            return comments