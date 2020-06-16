import boto3
from botocore.client import Config
import os

def norm(s):
	ns = ""
	last = "."
	for i in s:
		if i == "\\" and last != "\\":
			ns = ns + "/"
		elif i != "\\":
			ns = ns + i
		else:
			continue
		last = i
	return ns
# Initialize a session using DigitalOcean Spaces.
session = boto3.session.Session()
client = session.client('s3',
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id='ACCESS KEY',
                        aws_secret_access_key='SECRET KEY')

# List all buckets on your account.
response = client.list_buckets()
spaces = [space['Name'] for space in response['Buckets']]
print("Spaces List: %s" % spaces[0])
toUp = []
path = ""
for i in os.walk("."):
	for q in i:
		print(q)
		if isinstance(q, str):
			path = norm(q)
		else:
			if len(q) > 0:
				for n in q:
					toUp.append("{}/{}".format(path, n))

print(toUp)
for i in toUp:
	if os.path.isfile(i):
		resp = client.upload_file(i, spaces[0], i)
		print("{} completed: {}".format(i, resp))