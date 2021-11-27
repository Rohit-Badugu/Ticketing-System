from classes.utils import Utils

utils = Utils()

def test_dateTransform():
    formatted_date = "Nov 22, 2021 07:39 AM"
    assert utils.transformDate("2021-11-22T07:39:05Z") == formatted_date

def test_userIDs():
    tickets = [{
        "url": "https://zccrbadugu.zendesk.com/api/v2/tickets/1.json",
        "id": 1,
        "requester_id": 422082800711,
        "submitter_id": 422082799231,
        "assignee_id": 422082799231,
        },
        {
        "url": "https://zccrbadugu.zendesk.com/api/v2/tickets/2.json",
        "id": 1,
        "requester_id": 422082799231,
        "submitter_id": 422082799231,
        "assignee_id": 422082799231,
        }]
    result = utils.getUserIDs(tickets)
    userIDs = result.split(",")
    assert len(userIDs) == 2

