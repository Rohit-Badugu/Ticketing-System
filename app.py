from flask import Flask, render_template, request
import requests, ujson, math
from requests import api
from datetime import datetime

app = Flask(__name__)
num_tickets_in_page = 25

class Utils:
    def getUserIDs(self, tickets):
        userIDs = set()
        for ticket in tickets:
            requester_id = ticket["requester_id"]
            assignee_id = ticket["assignee_id"]
            userIDs.add(requester_id)
            userIDs.add(assignee_id)
        
        return ','.join(str(s) for s in userIDs)
        
    def getTicketUserIDs(self, ticket, comments):
        userIDs = set()
        requester_id = ticket["requester_id"]
        assignee_id = ticket["assignee_id"]
        userIDs.add(requester_id)
        userIDs.add(assignee_id)
        for comment in comments:
            userIDs.add(comment["id"])
            
        return ','.join(str(s) for s in userIDs)
        
    def transformDate(self, dateStr):
        dateObj = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
        return dateObj.strftime("%m/%d/%Y %H:%M")

    def createPayload(self, tickets, users, groups, count, page_no):
        userMap = {}
        groupMap = {}
        payload = {}
        for user in users:
            userMap[user["id"]] = user["name"]
        for group in groups:
            groupMap[group["id"]] = group["name"]
        for ticket in tickets:
            ticket["updated_at"] = self.transformDate(ticket["updated_at"])
            ticket["requester"] = userMap[ticket["requester_id"]]
            ticket["assignee"] = userMap[ticket["assignee_id"]]
            ticket["group"] = groupMap[ticket["group_id"]]
        
        pageCount = len(tickets)
        offset = (page_no-1)*num_tickets_in_page
        numOfPages = math.ceil(count/num_tickets_in_page)

        payload["tickets"] = tickets
        payload["totalCount"] = count
        payload["startCount"] = offset+1
        payload["endCount"] = offset + pageCount
        
        if page_no == 1:
            payload["prevActive"] = False
        else:
            payload["prevActive"] = True
        if page_no == numOfPages:
            payload["nextActive"] = False
        else:
            payload["nextActive"] = True

        payload["page_no"] = page_no
        return payload

    def createTicketPayload(self, ticket, comments, users):
        userMap = {}
        payload = {}
        for user in users:
            userMap[user["id"]] = user["name"]
        for comment in comments:
            comment["created_at"] = self.transformDate(comment["created_at"])
            comment["authorName"] = userMap[comment["author_id"]]
        
        payload["comments"] = comments
        payload["ticket"] = ticket
        return payload




class ApiClient:
    _instance = None    #Singleton class
    host = "https://zccrbadugu.zendesk.com/"
    headers = {"Authorization": "Basic cmJhZHVndUBhc3UuZWR1L3Rva2VuOmRIR1YzbHYxbzRlSHlGNnJtR2NmZVF0UmNxaXJxZDN4MXhDWGtHMU0="}

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



@app.route('/')
def index():
    page_no = request.args.get("page")
    if page_no == None:
        page_no = 1
    page_no = int(page_no)
    queryHandler = QueryHandler()
    utils = Utils()

    jsonResponse = queryHandler.fetchTickets(page_no)
    tickets = jsonResponse["tickets"]
    users = queryHandler.fetchUserInfo(tickets)
    groups = queryHandler.fetchGroups()
    payload = utils.createPayload(tickets, users, groups, jsonResponse["count"], page_no)

    return render_template('index.html', payload=payload)


@app.route('/ticket')
def detail():
    queryHandler = QueryHandler()
    utils = Utils()

    ticket_id = request.args.get("id")
    ticket = queryHandler.fetchTicketInfo(ticket_id)
    comments = queryHandler.fetchComments(ticket_id)
    users = queryHandler.fetchTicketUsers(ticket, comments)
    payload = utils.createTicketPayload(ticket, comments, users)

    return render_template('ticket.html', payload=payload)


if __name__ == "__main__":
    app.run()