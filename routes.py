from flask import render_template, request
from classes.queryHandler import QueryHandler
from classes.utils import Utils

def configure_routes(app):
    @app.route('/test')
    def test():
        return "Success"

    @app.route('/')
    def index():

        try:
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
        except TypeError:
            return render_template('404.html'), 404

        return render_template('index.html', payload=payload)


    @app.route('/ticket')
    def detail():
        queryHandler = QueryHandler()
        utils = Utils()

        try:
            ticket_id = request.args.get("id")
            if ticket_id == None or ticket_id == "":
                return render_template('404.html'), 404

            ticket = queryHandler.fetchTicketInfo(ticket_id)
            comments = queryHandler.fetchComments(ticket_id)
            users = queryHandler.fetchTicketUsers(ticket, comments)
            payload = utils.createTicketPayload(ticket, comments, users)
        except TypeError:
            return render_template('404.html'), 404

        return render_template('ticket.html', payload=payload)
        
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404