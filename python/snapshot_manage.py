#!/usr/bin/python
__author__ = "Jeeva Kailasam"
__version__ = "1.0"
__email__ = "jkailasam@netflix.com"
__status__ = "Development"



### Define the required configuration here
config = {

    # AWS credentials for the IAM user (alternatively can be set up as environment variables)
    # 'aws_access_key': 'xxxxxxxx',
    # 'aws_secret_key': 'xxxxxxxxxxxx',

    # EC2 info about your server's region
    'ec2_region_name': 'us-west-1',
    'ec2_region_endpoint': 'ec2.us-west-2.amazonaws.com',

    # Tag of the EBS volume you want to take the snapshots of
    'tag_name': 'tag:MakeSnapshot',
    'tag_value': 'True',

    # Number of snapshots to keep (the older ones are going to be deleted,
    # since they cost money).
    'keep_day': 6,
    'keep_week': 4,
    'keep_month': 2,

    # Path to the log for this script
    'log_file': '/tmp/makesnapshots.log',

    # ARN of the SNS topic (optional)
    #'arn': 'xxxxxxxxxx',

    # Proxy config (optional)
    #'proxyHost': '10.100.x.y',
    #'proxyPort': '8080'
}

### Import modules
import sys
import datetime
import argparse
import time
import boto.ec2
import boto.sns



region = config['ec2_region_name']
print region



conn = boto.ec2.connect_to_region(args.region)
# vols = conn.get_all_volumes(filters={ 'tag:' + config['tag_name']: config['tag_value'] })
vols = conn.get_all_volumes(filters={ 'tag:Name': 'tenfootui-final-sda1-v1' })

for vol in vols:
    
