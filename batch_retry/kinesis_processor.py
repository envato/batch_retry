import uuid
import json
import logging
import boto3

class KinesisProcessor(object):
    """
    Batch send data to Kinesis with the PutRecords api method
    Data is json encoded before being sent to Kinesis
    A random partition key is generated for each record
    """
    def __init__(self, kinesis_client, stream, batch_size=250):
        self.kinesis_client = kinesis_client
        self.stream = stream
        self.batch_size = batch_size

    def send(self, raw_records):
        """
        Send records to Kinesis
        """
        batches = [raw_records[index:index + self.batch_size] for index in range(0, len(raw_records), self.batch_size)]
        failed_records = []
        for batch in batches:
            records = self.__build_records(batch)
            resp = self.kinesis_client.put_records(
                StreamName=self.stream,
                Records=records
            )
            logging.info("Data sent to Kinesis: %s", resp)
            failed_records = failed_records + self.__extract_failed_records(records, resp)

        return failed_records

    def __extract_failed_records(self, records, put_records_response):
        failed_records = []
        if put_records_response['FailedRecordCount'] == 0:
            return failed_records

        for index in range(len(records)):
            send_information = put_records_response['Records'][index]
            record = records[index]
            if 'ErrorCode' in send_information:
                logging.debug("Record send to Kinesis failed: %s:%s", send_information['ErrorCode'], send_information['ErrorMessage'])
                failed_records.append(record)

        return failed_records

    def __build_records(self, batch):
        partition_key = uuid.uuid4().hex
        return list(map(lambda x: {'Data': json.dumps(x), 'PartitionKey': partition_key}, batch))
