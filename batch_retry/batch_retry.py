import time

class RetryWithExponentialBackoff(object):
    """
    Retry a function a pre-defined number of times, with exponential backoff.
    Any results returned from the function are assumed to be records that need to be retried.
    """
    def __init__(self, send_function, retries=5):
        self.retries = retries
        self.send_function = send_function

    def send_with_retries(self, records_to_send):
        """
        Send records using the previously defined function.
        Returns True or False depending on if it succeeded.
        """
        attempts = 0
        successful = False
        while attempts < self.retries:
            failed_records = self.send_function(records_to_send)
            if len(failed_records) == 0:
                successful = True
                break

            attempts += 1
            records_to_send = failed_records

            # Taken from the AWS example for Exponential Backoff
            # http://docs.aws.amazon.com/general/latest/gr/api-retries.html
            wait_time = (2 ** attempts) * 100
            time.sleep(wait_time)

        return successful
