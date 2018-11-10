import boto3
import slackweb 

lst = ["SEC", "Build", "Riq", "IQC", "ECP-Prod", "ECP-Staging", "SFDC-SIQ-Staging", "SFDC-SIQ-Prod", "Databricks-Admin", "Analytics-Legacy"]


def slack_call(i): 
         slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
         slack.notify(text=str(i)+" is publicly visible")

def bucket_check(account,client):
   #slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
   slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
   slack.notify(text="==============================================")
   slack.notify(text="`Public S3 buckets in the "+str(account)+" Account`")
   slack.notify(text="==============================================")
   #print("***************",i,"*****************")
   bucket_name = list()
   public_bucket = list()
   response = client.list_buckets()

   for i in response['Buckets']:
      if not i['Name'] in bucket_name: bucket_name.append(i['Name'])
      else: continue
   
   for i in bucket_name:
      response = client.get_bucket_acl(
      Bucket = i
      )
      for j in response['Grants']:
          if "URI" in j['Grantee'] and not "LogDelivery" in j['Grantee']['URI']: 
             if not i in public_bucket: public_bucket.append(i)
             else: continue

   for i in public_bucket:
       #print(i,"is publicly visible")
        slack_call(i)

for i in lst:
   session = boto3.Session(profile_name=i,region_name='us-west-2')
   client = session.client('s3')
   bucket_check(i,client)
         
