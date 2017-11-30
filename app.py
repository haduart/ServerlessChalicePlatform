from chalice import Chalice, NotFoundError, Response
import os
import boto3
import logging

app = Chalice(app_name='platform')

app.log.setLevel(logging.DEBUG)
app.debug = True

MOVIE_TABLE = os.getenv('APP_TABLE_NAME', 'Movies6')
table = boto3.resource('dynamodb').Table(MOVIE_TABLE)


@app.lambda_function()
def realtime_lambda_function(event, context):
    app.log.debug("This call is from the Lambda")

    title = "The Big New Movie"
    year = 2015

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
    app.log.debug("print: Data persisted")
    return "test"


@app.route('/lambda')
def insert_data_in_lambda():
    return realtime_lambda_function(None, None)


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
