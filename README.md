# snaphotanyzer-30000

Demo Project to manage ec2 instance snapshots

## About

This project is a Demo, and uses boto3 to manage AWS EC2 instance snapshots

## Configuring

shotty uses the configuration file created by the AWS cli.  e.g.

`aws configure --profile shotty`

## Running

`pipenv run "python shotty.shotty.py <command> <subcommand> <--project=PROJECT>"`

*command* is instances, volumes, or snapshots
*subcommand* instances (list, start, stop, snapshot)
*subcommand* volumes (list
*subcommand* snapshots (list)
*project* is optional
