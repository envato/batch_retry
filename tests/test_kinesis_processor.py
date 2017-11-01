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

        self.uuid_patch = patch('uuid.uuid4')
        self.uuid_mock = self.uuid_patch.start()
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

        self.logging_info_patch = patch('logging.info')
        self.logging_info_mock = self.logging_info_patch.start()

        self.time_patch = patch('time.sleep')
        self.time_mock = self.time_patch.start()

    def tearDown(self):
        self.uuid_patch.stop()
        self.logging_info_patch.stop()
        self.time_patch.stop()

    def __build_kinesis_call(self, event):
        return call(Records=[{'Data': json.dumps(event), 'PartitionKey': self.hex}], StreamName=self.stream_name)

    def __send_events(self, events):
        KinesisProcessor(self.kinesis_client_mock, self.stream_name, batch_size=1).send(events)

    def test_puts_events_on_the_kinesis_stream(self):
        self.__send_events([self.event_1])
        expected = [self.__build_kinesis_call(self.event_1)]
        actual = self.kinesis_client_mock.put_records.mock_calls
        self.assertListEqual(expected, actual)

    def test_puts_events_on_the_kinesis_stream_in_batches(self):
        self.__send_events([self.event_1, self.event_2])
        expected = [self.__build_kinesis_call(self.event_1), self.__build_kinesis_call(self.event_2)]
        actual = self.kinesis_client_mock.put_records.mock_calls
        self.assertListEqual(expected, actual)

    def test_logs_the_kinesis_stream_response(self):
        self.__send_events([self.event_1])
        expected = [call("Data sent to Kinesis: %s", self.kinesis_response)]
        actual = self.logging_info_mock.mock_calls
        self.assertListEqual(expected, actual)
