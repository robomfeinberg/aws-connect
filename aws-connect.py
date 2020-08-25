#!/usr/bin/env python3

import boto3
import botocore
import sys
import os
import argparse
import gimme_aws_creds.main
import gimme_aws_creds.ui
from tabulate import tabulate
from botocore.exceptions import ClientError, ParamValidationError

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', default="", type=str, help='Client project name to use.')
    parser.add_argument('-p', '--profile', default="default", type=str, help='This is the RMG Account/Profile. This should almost always be left as the default')
    parser.add_argument('-r', '--role', default='00000000000', type=str, help='AWS Account ID, The default is default')
    args = parser.parse_args()

    client = args.client
    profile = args.profile
    role = args.role

    os.environ['AWS_PROFILE'] = profile
    os.environ['AWS_DEFAULT_PROFILE'] = profile

    print("Profile being used " + profile)
    if client :
          print("Client name is " + client)

    if authcheck():
        print("==================================================================")
        print(" ")
    else:
        print("Auth Failure or something went wrong")
        gimme(profile, role)

    listec2(profile)


def listec2(profile):
    session = boto3.session.Session(profile_name=profile)
    ec2 = session.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    fortab = []
    for i in instances:
        name = ""
        for tag in i.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
        fortab.append([name, i.public_ip_address, i.private_ip_address, i.instance_id])
    print(tabulate(fortab, ['Name', 'Public IP', 'Private IP', 'InstanceID']))
    print(boto3.client('sts').get_caller_identity())
    print("============")
    print(boto3.session.Session())

def authcheck():
    sts = boto3.client('sts')
    try:
        sts.get_caller_identity()
        print("Credentials are valid.")
        return True
    except ClientError as e:
        print("Credentials are NOT valid.")   
        print("Error: %s" % e)
        return False

def gimme(profile, role):
    account_ids = sys.argv[1:] or [
    #account_ids = role or [
    '00000000000',
    #'XXXXXXXXXXXX',
    ]
    pattern = "|".join(sorted(set(account_ids)))
    pattern = '/:({}):/'.format(pattern)
  
    ui = gimme_aws_creds.ui.CLIUserInterface(argv=[sys.argv[0], '--role', pattern])    
    creds = gimme_aws_creds.main.GimmeAWSCreds(ui=ui)

    # Print out all selected roles:
    for role in creds.aws_selected_roles:
        print(role)
        #print("The role being used is " + role)

    # Generate credentials overriding profile name with `okta-<account_id>`
    for data in creds.iter_selected_aws_credentials():
        arn = data['role']['arn']
        account_id = None
        for piece in arn.split(':'):
            if len(piece) == 12 and piece.isdigit():
                account_id = piece
                break
    
        if account_id is None:
            raise ValueError("Didn't find aws_account_id (12 digits) in {}".format(arn))

        # We want our credentials profile name to match the account/aws profile name    
        #data['profile']['name'] = 'okta-{}'.format(account_id)
        data['profile']['name'] = '{}'.format(profile)
        creds.write_aws_creds_from_data(data)    

if __name__ == "__main__":
  main()