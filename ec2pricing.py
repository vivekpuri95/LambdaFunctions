import boto3
import pprint
import json

regionList={
	'us-east-2':'US East (Ohio)',
	'us-east-1':'US East (N. Virginia)',
	'us-west-1':'US West (N. California)',
	'us-west-2':'US West (Oregon)',
	'ap-northeast-1':'Asia Pacific (Tokyo)',
	'ap-northeast-2':'Asia Pacific (Seoul)',
	'ap-south-1':'Asia Pacific (Mumbai)',
	'ap-southeast-1':'Asia Pacific (Singapore)',
	'ap-southeast-2':'Asia Pacific (Sydney)',
	'ca-central-1':'Canada (Central)',
	'cn-north-1':'China (Beijing)',
	'cn-northwest-1':'China (Ningxia)',
	'eu-central-1':'EU (Frankfurt)',
	'eu-west-1':'EU (Ireland)',
	'eu-west-2':'EU (London)',
	'eu-west-3':'EU (Paris)',
	'us-gov-west-1':'AWS GovCloud (US)'
}
	
def ec2Prices(event,context):
	instanceType = event['key1'] 
	region = event['key2']  
	os = event['key3']
	print(instanceType)
	print(region)
	print(os)
	
	client = boto3.client('pricing',aws_access_key_id="<access_key>",aws_secret_access_key="<secret_key>", region_name="us-east-1")
	response = client.get_products(
		ServiceCode='AmazonEC2',
		Filters=[						#filters are added here
			{
				'Type': 'TERM_MATCH',
				'Field': 'instanceType',
				'Value': instanceType
			},
			{
				'Type': 'TERM_MATCH',
				'Field': 'operatingSystem',
				'Value': os
			},
			{
				'Type': 'TERM_MATCH',
				'Field': 'location',
				'Value': regionList[region]
			},
			{
				'Type': 'TERM_MATCH',
				'Field': 'preInstalledSw',
				'Value': 'NA'
			},
			{
				'Type': 'TERM_MATCH',
				'Field': 'tenancy',
				'Value': 'shared'
			},
			{
				'Type': 'TERM_MATCH',
				'Field': 'licenseModel',
				'Value': 'No License required'
			}
		]
	)									#extracting price from garbage
	response=response['PriceList'][0]
	jsonwala=json.loads(response)		#convert unicode to json
	jsonwala=jsonwala['terms']['OnDemand']
	for key in jsonwala:
		jsonwala=jsonwala[key]
		break;
	jsonwala=jsonwala['priceDimensions']
	for key in jsonwala:
		jsonwala=jsonwala[key]
		break;
	jsonwala=jsonwala['pricePerUnit']['USD']
	return jsonwala

# SAMPLE RUN
# Permitted OS: Linux;RHEL;Windows;SUSE
# Fixed for on-demand pricing
#def lambda_handler(event, context):
#	response=ec2Prices('m4.xlarge','ap-south-1','Windows')print response

#OUTPUT FOR DEBUGGING AND FILTER CUSTOMIZATION, REMOVE BEFORE LIVE
#pp = pprint.PrettyPrinter(indent=4, depth=10, stream=None)
#for i in response:
#	i=json.loads(i)
#	pp.pprint(i['product'])
#	pp.pprint(i['terms']['OnDemand']);

