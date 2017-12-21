"""
This script is for testing/calling in several different ways
functions from QRColorChecker modules.


@author: Eduard Cespedes Borràs
@mail: eduard@iot-partners.com
"""

import unittest
from chalicelib.server import Server
import sys

sys.path.append('../chalicelib')


class AppTest(unittest.TestCase):

    def setUp(self):
        self.sns_client = TestSNS()
        self.log = TestLog()
        self.dynamodb = TestDynamoDB()

    def test_publishing_data_to_SNS(self):
        server = Server(None, self.sns_client, self.log)
        expected_message = "Good news everyone!"
        server.publish_data()
        self.assertEqual(1, self.sns_client.return_published_times())
        self.assertEqual(expected_message, self.sns_client.return_message())

    def test_persist_data_to_DynamoDB(self):
        server = Server(self.dynamodb, None, self.log)
        expected_item = {
            'title': "The Big New Movie",
            'year': 2015,
            'info': {
                'plot': "Nothing happens at all.",
                'rating': "0"
            }
        }
        server.persist_data()
        self.assertEqual(1, self.dynamodb.return_persisted_times())
        self.assertEqual(expected_item, self.dynamodb.return_persisted_item())


class TestLog:

    def __init__(self):
        self.message = ''
        self.logged = 0

    def debug(self, message):
        self.message = message
        self.logged += 1
        return message

    def return_message(self):
        return self.message

    def return_logging_times(self):
        return self.logged


class TestSNS:

    def __init__(self):
        self.Message = ''
        self.TopicArn = ''
        self.Subject = ''
        self.published = 0

    def publish(self, TopicArn, Subject, Message):
        self.Message = Message
        self.TopicArn = TopicArn
        self.Subject = Subject
        self.published += 1

    def return_message(self):
        return self.Message

    def return_published_times(self):
        return self.published


class TestDynamoDB:

    def __init__(self):
        self.Item = ''
        self.persisted = 0

    def put_item(self, Item):
        self.Item = Item
        self.persisted += 1

    def return_persisted_item(self):
        return self.Item

    def return_persisted_times(self):
        return self.persisted
