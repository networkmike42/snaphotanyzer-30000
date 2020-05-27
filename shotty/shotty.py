import boto3
import sys
# sys.argv puts the command line into a list so you can parse the arguments
import click
# a better way of parsing the command line arguments

# Set up the Boto session
session = boto3.Session(profile_name='shotty')
# set ec2 to use the boto session and call the ec2 resource
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
# the filter has a name which is what you want to filter on (in this case the tag is Project), only return matching projects
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
# if there is no project, return all the instances
        instances = ec2.instances.all()
    return instances

# this hands off arguments when to this function click
@click.group()
# takes the commands
def instances():
    """Commands for instances"""
# when the command is list
# shotty.py list --project=Valkyrie
@instances.command('list')
@click.option('--project', default=None, help="Only instances for projects (tag Project:<name>)")
# Call ec2 looking for instances all
def list_instances(project):
# This is for click
    "List EC2 instances"
    instances = []

    if project:
# the filter has a name which is what you want to filter on (in this case the tag is Project), then an acceptable value
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
# clean up the tags so it is just key / value dictionary instead of a list
        tags = { t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
# if there is no project, it returns the second string
            tags.get('Project', '<no project>'),
            tags.get('Class', '<no class>'),
            )))

    return

# when the command is stop
# shotty.py stop --project=Valkyrie
@instances.command('stop')
@click.option('--project', default=None, help="Only instances for projects")
def stop_instances(project):
    "Stop EC2 instances"
# since the code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)

    for i in instances:
        print("Stoping {0}".format(i.id))
        i.stop()

# when the command is start
# shotty.py start --project=Valkyrie
@instances.command('start')
@click.option('--project', default=None, help="Only instances for projects")
def start_instances(project):
    "Start EC2 instances"
# since thes code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}".format(i.id))
        i.start()

if __name__ == "__main__":
    print(sys.argv)
# allows you to feed in commands and then arguments
    instances()
