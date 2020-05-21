import boto3
import sys
# sys.argv puts the command line into a list so you can parse the arguments
import click
# a better way of parsing the command line arguments

# Set up the Boto session
session = boto3.Session(profile_name='shotty')
# set ec2 to use the boto session and call the ec2 resource
ec2 = session.resource('ec2')

# this hands off when to call this function to click
@click.command()
# Call ec2 looking for instances all
def list_instances():
# This is for click
    "List EC2 instances"
    for i in ec2.instances.all():
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name)))
    return



if __name__ == "__main__":
    print(sys.argv)
    list_instances()
