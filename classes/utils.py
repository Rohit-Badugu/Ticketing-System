import math
from datetime import datetime
num_tickets_in_page=25

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
        return dateObj.strftime("%b %d, %Y %H:%M %p")

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
            userMap[user["id"]] = {"name": user["name"], "photo_url": user["photo"]["content_url"]}
        for comment in comments:
            comment["created_at"] = self.transformDate(comment["created_at"])
            userEntry = userMap[comment["author_id"]]
            comment["authorName"] = userEntry["name"]
            comment["photo_url"] = userEntry['photo_url']
        
        ticket["requesterName"] = userMap[ticket["requester_id"]]["name"]
        ticket["assigneeName"] = userMap[ticket["assignee_id"]]["name"]

        payload["comments"] = comments
        payload["commentCount"] = len(comments)
        payload["ticket"] = ticket
        return payload