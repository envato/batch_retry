# Kinesis Batch Retry

This library provides an interface to submit a batch of records to Kinesis using the [PutRecords](http://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecords.html) API method, with retries and exponential backoff.

Usage:

```
from kinesis_batch_retry import KinesisBatchRetry

def main():
  kinesis_client = boto3.client('kinesis')
  kinesis_retry_client = KinesisBatchRetry(kinesis_client, batch_size=250, retries=5)
  kinesis_retry_client.send(['my_first_record'])
```

## Future enhancements

The same mechanism could be applied to Kinesis Firehose Delivery Streams. While they support much more records/s, making this less of a problem, it would be trivial to adapt the retry/backoff mechanism to that service.

## Development Status

Early stage use

## Installing

`pip install kinesis_batch_retry`

Or add it to your `requirements.txt` file

## Contributing

For bug fixes, documentation changes, and small features:  
1. Fork it ( https://github.com/envato/kinesis_batch_retry/fork )  
2. Create your feature branch (`git checkout -b my-new-feature`)  
3. Commit your changes (`git commit -am 'Add some feature'`)  
4. Push to the branch (`git push origin my-new-feature`)  
5. Create a new Pull Request  

For larger new features: Do everything as above, but first also make contact with the project maintainers to be sure your change fits with the project direction and you won't be wasting effort going in the wrong direction
