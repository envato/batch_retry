import json
import unittest
import uuid
import logging
from batch_retry import KinesisProcessor
from unittest.mock import patch, call, MagicMock

class TestKinesisProcessor(unittest.TestCase):
    def setUp(self):
        self.stream_name = 'stream'
        self.hex = 'hex'
        self.event_1 = {"SomeEvent1": "text1"}
        self.event_2 = {"SomeEvent2": "text2"}

        self.uuid_mock = patch('uuid.uuid4').start()
        self.uuid_mock().hex = self.hex

        self.kinesis_response = {
            'FailedRecordCount': 0,
            'Records': [
                {
                    'SequenceNumber': 'string',
                    'ShardId': 'string',
                }
            ],
            'EncryptionType': 'NONE'
        }
        self.kinesis_client_mock = MagicMock()
        self.kinesis_client_mock.put_records.return_value = self.kinesis_response

        self.logging_info_mock = patch('logging.info').start()

        patch('time.sleep').start()

    def tearDown(self):
        patch.stopall()

    def __build_kinesis_call(self, event):
        return call(Records=[{'Data': json.dumps(event), 'PartitionKey': self.hex}], StreamName=self.stream_name)

    def __send_events(self, events):
        KinesisProcessor(self.kinesis_client_mock, self.stream_name, batch_size=1).send(events)

    def test_puts_events_on_the_kinesis_stream(self):
        self.__send_events([self.event_1])
        self.kinesis_client_mock.put_records.assert_has_calls([self.__build_kinesis_call(self.event_1)])

    def test_puts_events_on_the_kinesis_stream_in_batches(self):
        self.__send_events([self.event_1, self.event_2])
        self.kinesis_client_mock.put_records.assert_has_calls([
            self.__build_kinesis_call(self.event_1),
            self.__build_kinesis_call(self.event_2)])

    def test_logs_the_kinesis_stream_response(self):
        self.__send_events([self.event_1])
        self.logging_info_mock.assert_called_with("Data sent to Kinesis: %s", self.kinesis_response)
