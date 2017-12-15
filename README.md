# Batch Retry

This library provides an interface to submit a batch of records to an API, which retries all failed records with an exponential backoff. Currently it just supports Kinesis using the [PutRecords](http://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecords.html) API method, but it can be used to support more APIs.

Usage:

```
from batch_retry import BatchRetry
from batch_retry import KinesisProcessor

def main():
  kinesis_client = boto3.client('kinesis')
  send_function = KinesisProcessor(kinesis_client, 'my-stream', batch_size=250).send
  BatchRetry(send_function, retries=5).send_with_retries(['my_first_record'])
```

## Development Status

We don't recommend using it in production

## Installing

`pip install batch_retry`

Or add it to your `requirements.txt` file

## Contributing

For bug fixes, documentation changes, and small features:  
1. Fork it ( https://github.com/envato/batch_retry/fork )  
2. Create your feature branch (`git checkout -b my-new-feature`)  
3. Commit your changes (`git commit -am 'Add some feature'`)  
4. Push to the branch (`git push origin my-new-feature`)  
5. Create a new Pull Request  

For larger new features: Do everything as above, but first also make contact with the project maintainers to be sure your change fits with the project direction and you won't be wasting effort going in the wrong direction

### Running tests

```
python setup.py test
```
