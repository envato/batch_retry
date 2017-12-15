from setuptools import setup

setup(
    name='batch_retry',
    version='0.0.2',
    license='MIT',
    author='patrickrobinson',
    author_email='patrick.robinson@envato.com',
    url='https://github.com/envato/batch_retry',
    long_description="README.md",
    packages=['batch_retry'],
    include_package_data=True,
    description="Batch send data with retries and exponential backoff",
    install_requires=[
        'boto3>=1.3.1,<2',
    ],
    suite='tests',
)
