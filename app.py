from chalice import Chalice
import boto3
import decimal

app = Chalice(app_name='platform')

@app.lambda_function()
def realtime_lambda_function(event, context):
    app.log.debug("This call is from the Lambda")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Movies')

    title = "The Big New Movie"
    year = 2015

    response = table.put_item(
        Item={
            'title': title,
            'year': year,
            'info': {
                'plot': "Nothing happens at all.",
                'rating': decimal.Decimal(0)
            }
        }
    )
    app.log.debug("Data persisted")
    return response


@app.route('/')
def index():
    app.log.debug("This call is from the API Gateway")
    return realtime_lambda_function(None, None)
