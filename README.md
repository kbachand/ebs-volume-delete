# ebs-volume-delete
A basic Python script that will list and delete orphaned EBS volumes in AWS.

## Setup
Follow the steps to get setup to utilize this script
* `git clone https://github.com/kbachand/ebs-volume-delete.git`
* `cd ebs-orphan-volume-delete`

## Script Usage
* `python3 ebs-orphan-volume-delete.py`  - Will display a list of snapshots to delete but will not delete any
* `python3 ebs-orphan-volume-delete.py --delete` - Deletes snapshots

## Requirements
* Python 3
* boto3
* awscli
