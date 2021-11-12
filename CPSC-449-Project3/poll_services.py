import hug
import boto3
import json
import requests

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

@hug.get("/polls/")
def polls():
    table = dynamodb.Table('poll')
    data = table.scan()
    polls = data['Items']

    while 'LastEvaluatedKey' in data:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        polls.extend(response['Items'])
    return polls

@hug.get("/polls/{id}")
def retrieve_poll(response, id: hug.types.number):
    table = dynamodb.Table('poll')
    try:
        data = table.get_item(
            Key = { "poll_id": id }
        )
        poll = data['Item']
    except:
        response.status = hug.falcon.HTTP_404
        poll = []
    return poll

@hug.delete("/polls/delete")
def delete_item(response, poll_id: hug.types.number):
    table = dynamodb.Table('poll')
    table.delete_item(
        Key={
            "poll_id": poll_id
        }
    )
    return response.status

@hug.post("/polls/create/", status=hug.falcon.HTTP_201)
def create_poll(response, poll_id: hug.types.number, title: hug.types.text, poll_responses):
    table = dynamodb.Table('poll')
    if type(poll_responses) == str:
        poll_responses = poll_responses.split(', ')
    print(poll_responses)
    poll = {
        "poll_id": poll_id,
        "title": title,
        "responses": poll_responses
    }
    try:
        table.put_item(Item=poll)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
    return response.status

@hug.get("/polls/vote/{id}")
def vote_poll(response, id: hug.types.number):
    poll = requests.get(f'http://127.0.0.1/polls/{id}')
    return poll
