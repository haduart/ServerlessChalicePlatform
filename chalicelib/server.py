"""
All the logic that can and should be tested will be here


@author: Eduard Cespedes Borràs
@mail: eduard@iot-partners.com
"""

from chalice import Chalice, NotFoundError, Response
import json
import boto3
import logging


class Server:
    def __init__(self, table, sns_client, log):
        self.table = table
        self.sns_client = sns_client
        self.log = log

    def publish_data(self):
        self.log.debug("This called from publish_data")
        self.sns_client.publish(
            TopicArn="arn:aws:sns:eu-west-1:488643450383:defaultSNS",
            Subject="Test from Lambda",
            Message="Good news everyone!"
        )
        return {"Published Event": "defaultSNS"}

    def persist_data(self, event=None, context=None):
        title = "The Big New Movie"
        year = 2015
        try:
            self.table.put_item(
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
        self.log.debug("print: Data persisted")
