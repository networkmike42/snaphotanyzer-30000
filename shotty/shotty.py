# boto3 allows you to work with AWS
# botocore deals with error messages from AWS
# sys.argv puts the command line into a list so you can parse the arguments
import sys
import boto3
import botocore

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
def cli():
    """Shotty does it all"""

# Defining a group to work with snapshots
@cli.group()
def snapshots():
    """Commands for snapshots"""
@snapshots.command('list')
@click.option('--project', default=None,
              help="Only snapshots for projects (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True,
              help="List all snapshots for each volume, not just the most recent")
# Call ec2 looking for snapshots with the instances
def list_snapshots(project, list_all):
# This is for click
    "List EC2 snapshots"
# since the code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
# .strftime("%c") to nicely format the time
                    s.start_time.strftime("%c")
                )))
# if the snapshot state matches leave this loop.  This will only get the first completed snapshot
                if s.state == 'completed' and not list_all:break
    return

# Defining a group based off the volumes command
@ cli.group('volumes')
def volumes():
    """Commands for volumes"""
@volumes.command('list')
@click.option('--project', default=None, help="Only volumes for projects (tag Project:<name>)")
# Call ec2 looking for volumes with the instances
def list_volumes(project):
# This is for click
    "List EC2 volumes"
# since the code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)
    for i in instances:
# for each volume in the instance
        for v in i.volumes.all():
            print(", ".join((
            v.id,
            i.id,
            v.state,
            str(v.size) + 'Gibs',
            v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return
# defining a group based off the instances command (ie instances.list, instances.stop, instances.start)
@cli.group('instances')
# takes the commands
def instances():
    """Commands for instances"""

# when the command is list
# shotty.py instances list --project=Valkyrie
@instances.command('list')
@click.option('--project', default=None, help="Only instances for projects (tag Project:<name>)")
# Call ec2 looking for instances all
def list_instances(project):
# This is for click
    "List EC2 instances"
# since the code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)
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
# shotty.py instances stop --project=Valkyrie
@instances.command('stop')
@click.option('--project', default=None, help="Only instances for projects")
def stop_instances(project):
    "Stop EC2 instances"
# since the code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)
    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print(" Could not stop {0}. ".format(i.id) + str(e))
            continue
    return

# when the command is start
# shotty.py instances start --project=Valkyrie
@instances.command('start')
@click.option('--project', default=None, help="Only instances for projects")
def start_instances(project):
    "Start EC2 instances"
# since thes code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)
    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Could not start {0}. ".format(i.id) + str(e))
            continue
    return
# when the command is snapshot
# shotty.py instances snapshot --project=Valkyrie
@instances.command('snapshot')
@click.option('--project', default=None, help="Create snapshots for all Volumes in project")
def create_snapshots(project):
    "create EC2 snapshots"
# since thes code is the same and reusable, create the function and call it instead of the code.
    instances = filter_instances(project)
    for i in instances:
# Stop the instance before taking a snapshot.  wait until its stopped
        print("Stopping instance {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("creating snapshot of instance {0}, Volume {1}".format(i.id, v.id))
            v.create_snapshot(Description="Created by SnapshotAlyzer 3000")
#start the instance back up and be sure its up before moving on to the next instance
        print("Starting instance {0}...".format(i.id))
        i.start()
        i.wait_until_running()
    print("jobs done!")
    return

# Here is the running program
if __name__ == "__main__":
    print(sys.argv)
# allows you to feed in commands and then arguments
    cli()
