from chalice import Chalice, NotFoundError, Response
import os
import boto3
import logging

app = Chalice(app_name='platform')

app.log.setLevel(logging.DEBUG)
app.debug = True

MOVIE_TABLE = os.getenv('APP_TABLE_NAME', 'defaultTable')
SNS_TOPIC = os.getenv('SNS_TOPIC', 'defaultSNS')

table = boto3.resource('dynamodb').Table(MOVIE_TABLE)
sns_client = boto3.client('sns')


@app.lambda_function()
def realtime_lambda_function(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    app.log.debug("This call is from the Lambda")
    app.log.debug("From SNS: " + event)

    title = "The Big New Movie"
    year = 2015

    try:
        response = table.put_item(
            Item={
                'title': title,
                'year': year,
                'info': {
                    'plot': "Nothing happens at all.",
                    'rating': "0"
                }
            }
        )
    except Exception as e:
        raise NotFoundError("Error adding an element on dynamodb")

    app.log.debug("print: Data persisted")
    return "test"


@app.route('/lambda')
def insert_data_in_lambda():
    sns_client.publish(
        TopicArn="arn:aws:sns:eu-west-1:488643450383:defaultSNS",
        Subject="Test from Lambda",
        Message="Good news everyone!"
    )
    return {"Published Event": "defaultSNS"}


@app.route('/')
def index():
    print("print: This call is from the API Gateway")
    return Response(body='hello world!',
                    status_code=200,
                    headers={'Content-Type': 'text/plain'})


@app.route('/roberto')
def roberto_function():
    app.log.debug("logging per la funcio del roberto")
    return {"hola": "roberto"}


OBJECTS = {
}


@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)
