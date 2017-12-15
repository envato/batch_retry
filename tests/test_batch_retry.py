import json
import unittest
from batch_retry import KinesisProcessor
from unittest.mock import patch, call, MagicMock
from batch_retry import BatchRetry

class TestKinesisProcessorWithRetries(unittest.TestCase):
    def setUp(self):
        self.stream_name = 'stream'
        self.event_1 = {"SomeEvent1": "text1"}
        self.event_2 = {"SomeEvent2": "text2"}
        self.put_records_attempts = 0

    def tearDown(self):
        patch.stopall()

    def mock_put_records_fail_first_attempt(self, **kwargs):
        if self.put_records_attempts == 0:
            self.put_records_attempts = 1
            return {
                'FailedRecordCount': 1,
                'Records': [
                    {
                        'SequenceNumber': 'string',
                        'ShardId': 'string',
                    },
                    {
                        'ErrorCode': 'string',
                        'ErrorMessage': 'string'
                    }
                ],
                'EncryptionType': 'NONE'
            }

        self.put_records_attempts = self.put_records_attempts + 1

        return {
            'FailedRecordCount': 0,
            'Records': [
                {
                    'SequenceNumber': 'string',
                    'ShardId': 'string',
                }
            ],
            'EncryptionType': 'NONE'
        }

    @patch('time.sleep')
    def test_puts_events_with_retries(self, MockSleep):
        kinesis_client_mock = MagicMock()
        kinesis_client_mock.put_records.side_effect = self.mock_put_records_fail_first_attempt
        send_function = KinesisProcessor(kinesis_client_mock, self.stream_name, batch_size=2).send
        BatchRetry(send_function).send_with_retries([self.event_1, self.event_2])
        self.assertEqual(2, self.put_records_attempts)

    @patch('time.sleep')
    def test_sleeps_for_milliseconds(self, MockSleep):
        kinesis_client_mock = MagicMock()
        kinesis_client_mock.put_records.side_effect = self.mock_put_records_fail_first_attempt
        send_function = KinesisProcessor(kinesis_client_mock, self.stream_name, batch_size=2).send
        BatchRetry(send_function).send_with_retries([self.event_1, self.event_2])
        MockSleep.assert_called_once_with(0.2)
