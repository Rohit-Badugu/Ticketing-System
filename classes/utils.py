import math
from datetime import datetime
from config import Config

num_tickets_in_page=Config.num_tickets_in_page

class Utils:
    #Loops through all the tickets to extract the user IDS of requester and assignee
    #The userIDs are joined to form a comma seperated string
    def getUserIDs(self, tickets):
        userIDs = set()
        for ticket in tickets:
            requester_id = ticket["requester_id"]
            assignee_id = ticket["assignee_id"]
            userIDs.add(requester_id)
            userIDs.add(assignee_id)
        
        return ','.join(str(s) for s in userIDs)

    #Loops through a ticket and comments to extract the user IDS of requester and assignee
    #The userIDs are joined to form a comma seperated string    
    def getTicketUserIDs(self, ticket, comments):
        userIDs = set()
        requester_id = ticket["requester_id"]
        assignee_id = ticket["assignee_id"]
        userIDs.add(requester_id)
        userIDs.add(assignee_id)
        for comment in comments:
            userIDs.add(comment["id"])
            
        return ','.join(str(s) for s in userIDs)
    
    #Transform dates from timestamp format to human readable format like Sep 20, 2021 09:00 AM
    def transformDate(self, dateStr):
        dateObj = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
        return dateObj.strftime("%b %d, %Y %H:%M %p")

    def capitalize(self, str):
        if str is None:
            return "None"
        return str.capitalize()

    #Parsing tickets, users, group objects to create a single payload to send to UI
    def createPayload(self, tickets, users, groups, count, page_no):
        userMap = {}
        groupMap = {}
        payload = {}

        for user in users:
            userMap[user["id"]] = user["name"]
        for group in groups:
            groupMap[group["id"]] = group["name"]
        
        #Looping through all the tickets and adding user and group names
        for ticket in tickets:
            #transforming date into more readable format
            ticket["updated_at"] = self.transformDate(ticket["updated_at"])

            #Adding names to ticket
            ticket["requesterName"] = userMap[ticket["requester_id"]]
            ticket["assigneeName"] = userMap[ticket["assignee_id"]]
            ticket["groupName"] = groupMap[ticket["group_id"]]

            #Function is created since the value of status/priority can be None
            ticket["status"] = self.capitalize(ticket["status"])
            ticket["priority"] = self.capitalize(ticket["priority"])
        
        pageCount = len(tickets)
        offset = (page_no-1)*num_tickets_in_page
        numOfPages = math.ceil(count/num_tickets_in_page)

        payload["tickets"] = tickets
        payload["totalCount"] = count
        payload["startCount"] = offset+1
        payload["endCount"] = offset + pageCount
        
        #Enabling/disabling prev and next buttons for pagination
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

    #Parsing ticket, users, and comments objects to create a single payload to send to UI
    def createTicketPayload(self, ticket, comments, users):
        userMap = {}
        payload = {}

        for user in users:
            userMap[user["id"]] = {"name": user["name"], "photo_url": user["photo"]["content_url"]}
        for comment in comments:
             #transforming date into more readable format
            comment["created_at"] = self.transformDate(comment["created_at"])
            userEntry = userMap[comment["author_id"]]
            comment["authorName"] = userEntry["name"]
            comment["photo_url"] = userEntry['photo_url']

        #Adding names to ticket
        ticket["requesterName"] = userMap[ticket["requester_id"]]["name"]
        ticket["assigneeName"] = userMap[ticket["assignee_id"]]["name"]
        statusStr = ticket["status"]
        ticket["status"] = self.capitalize(statusStr)

        payload["comments"] = comments
        payload["commentCount"] = len(comments)
        payload["ticket"] = ticket

        return payload