"""Lambda function to index S3 logs such as CloudTrail into AWS ES."""

import boto3
import gzip
import json
import os
from aws_requests_auth import boto_utils
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

host = os.environ['ES_HOST']
region = os.environ['ES_REGION']
index_name = os.environ['ES_INDEX_NAME']

auth = AWSRequestsAuth(
    aws_host=host,
    aws_region=region,
    aws_service='es',
    **boto_utils.get_credentials())

es = Elasticsearch(
    host=host,
    port=443,
    use_ssl=True,
    connection_class=RequestsHttpConnection,
    http_auth=auth)

s3 = boto3.client('s3')


def lambda_handler(event, context):
    """Main Lambda function."""
    print("Received event")
    # attribute bucket and file name/path to variables
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # where to save the downloaded file
    file_path = '/tmp/ctlogfile.gz'

    # downloads file to above path
    s3.download_file(bucket, key, file_path)

    # opens gz file for reading
    gzfile = gzip.open(file_path, "r")

    # loads contents of the Records key into variable (our actual cloudtrail
    # log entries!)
    response = json.loads(gzfile.readlines()[0])["Records"]

    # loops over the events in the json
    for i in response:
        print 'Sending event to elasticsearch'

        # adds @timestamp field = time of the event
        i["@timestamp"] = i["eventTime"]

        # removes .aws.amazon.com from eventsources
        i["eventSource"] = i["eventSource"].split(".")[0]
        data = json.dumps(i)

        # defines correct index name based on eventTime, so we have an
        # index for each day on ES
        event_date = i["eventTime"].split("T")[0].replace("-", ".")
        index = "{}-{}".format(index_name, event_date)

        res = es.index(index=index, doc_type="cloudtrail", body=data)
        print(res['created'])
    print "all done for this file!"
