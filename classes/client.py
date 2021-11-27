import requests, ujson
from config import Config

class ApiClient:
    _instance = None    #Singleton class
    host = "https://zccrbadugu.zendesk.com/"
    headers = {"Authorization": Config.API_KEY}

    def __init__(self):
        if ApiClient._instance != None:
            raise Exception("This is a singleton class")
        else:
            ApiClient._instance = self

    @staticmethod
    def getInstance():
        if ApiClient._instance == None:
            ApiClient()
        return ApiClient._instance

    def getTicketCount(self, endpoint):
        response = requests.get(ApiClient.host + endpoint, headers=ApiClient.headers)
        status = response.status_code
        if status == 200:
            jsonObject = ujson.loads(response.text)
            count = jsonObject["count"]["value"]
            return count

    def getTickets(self, endpoint, page_no):
        params = {"per_page": 25, "page": page_no}
        response = requests.get(ApiClient.host + endpoint, headers=ApiClient.headers, params=params)
        status = response.status_code
        if status == 200:
            jsonResponse = ujson.loads(response.text)
            return jsonResponse

    def getTicketInfo(self, endpoint):
        response = requests.get(ApiClient.host + endpoint, headers=ApiClient.headers)
        status = response.status_code
        if status == 200:
            jsonResponse = ujson.loads(response.text)
            ticket = jsonResponse["ticket"]
            return ticket

    def getUserInfo(self, endpoint, userIDs):
        params = {"ids": userIDs}
        response = requests.get(ApiClient.host + endpoint, headers=ApiClient.headers, params=params)
        status = response.status_code
        if status == 200:
            jsonObject = ujson.loads(response.text)
            userList = jsonObject["users"]
            return userList

    def getGroups(self, endpoint):
        response = requests.get(ApiClient.host + endpoint, headers=ApiClient.headers)
        status = response.status_code
        if status == 200:
            jsonObject = ujson.loads(response.text)
            groups = jsonObject["groups"]
            return groups

    def getComments(self, endpoint):
        response = requests.get(ApiClient.host + endpoint, headers=ApiClient.headers)
        status = response.status_code
        if status == 200:
            jsonObject = ujson.loads(response.text)
            comments = jsonObject["comments"]
            return comments