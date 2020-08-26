# aws-connect

AWS Connect is a test tool that will allow you to authenticate through okta and connect to your various AWS resources and multiple accounts. This will be also be setup to use AWS Instance Connect to ssh you into the system of your choice with automatic whitelisting and bastion hops.

## Requirements
* python 3.8
* pip3
* awscli 2.x
* MacOS or Linux
* aws-gimme-creds (https://github.com/Nike-Inc/gimme-aws-creds)
* Ec2 Instance Connect CLI (https://github.com/aws/aws-ec2-instance-connect-cli)
* AWS and Okta integration (https://help.okta.com/en/prod/Content/Topics/DeploymentGuides/AWS/aws-deployment.htm)


Install the requirements
```
pip3 install -r requirements.txt --user
```

### Configure gimme-aws-creds and awscli


```

# configure AWSCLI
# default
aws configure set default.region us-east-1
aws configure set default.output text
aws configure set default.cli_pager ""

# companyname (friendly AWS account name)
aws configure --profile companyname set role_arn arn:aws:iam::00000000000:role/GlobalAdmins
aws configure --profile companyname set output text
aws configure --profile companyname set source_profile rmgmedia
aws configure --profile companyname set cli_pager ""

```


More to follow. 
Missing key file examples and awscli/gimme-creds setup instructions 