# Serverless function for AWS to send CloudTrail logs from S3 to ElasticSearch
This lambda function will retreive CloudTrail logs from S3 and write them into an AWS ElasticSearch Domain
## Installation

1. serverless install -u https://github.com/EffectiveDevOpsWithAWS/serverless-cloudtrail-to-es -n cloudtrail-aws-es
2. Configure the [Environment variables of the function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/cloudtrail-aws-es-dev-lambda_handler?tab=code)
3. Configure the [triggers to be the S3 bucket where Cloudtrail write its logs to](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/cloudtrail-aws-es-dev-lambda_handler?tab=triggers)
4. Create a new index pattern in Kibana for `logstash-cloudtrail-*`
