import boto3
from pprint import pprint
import os
import sys
import argparse

ARG_HELP ="""
    --------------------------------------------------------------------------------
    Use to this EBS Orphan Volume Delete Script to delete Volumes that aren't in use

    Script Usage:
        python3 ebs-orphan-volume-delete.py (This is a dry run and will not delete any volumes)
        python3 ebs-orphan-volume-delete.py --delete
        ** Without --delete appended to cli command this script will not delete volumes **
    --------------------------------------------------------------------------------
    """
ec2_client = boto3.client('ec2')

# Variable defined to store unused volumes to delete
volumes_to_delete = list()

# Utilize describe_volumes() method to get details of each volume
volume_detail = ec2_client.describe_volumes()

# Displays each volume and its details
if volume_detail['ResponseMetadata']['HTTPStatusCode'] == 200:
    for volume in volume_detail['Volumes']:
        # Volume details
        print("Volume_id: ", volume['VolumeId'])
        print("Volume State: ", volume['State'])
        print("Attachment state length: ", len(volume['Attachments']))
        print(volume['Attachments'])
        print("--------------------------------------------")

        # Volumes without 'Attachments' and state is 'Available' are considered unused and can be qued for deletion.
        if len(volume['Attachments']) == 0 and volume['State'] == 'available':
            volumes_to_delete.append(volume['VolumeId'])

# Displays unused volumes to delete
print("Total unused volumes:",len(volumes_to_delete))

# Display profile and region infomation where data is being pulled from
session = boto3.Session()
print("Profile: ", session.profile_name)
print("Region: ", session.region_name)

# Deletion
total_errors = list()
total_deleted = list()
#deletion = input('Enter yes to proceed with deletion').lower()

#if deletion flag is specificed:
def delete(args):
    if args.delete is True and len(volumes_to_delete) > 0:
        for volume_id in volumes_to_delete:
            try:
                print("Deleting Volume with volume_id: " + volume_id)
                response = ec2_client.delete_volume(
                    VolumeId=volume_id
                )
                total_deleted.append(volume_id)
            except Exception as e:
                total_errors.append(volume_id)
                print("Issue in deleting volume with id: " + volume_id + " error is: " + str(e))

        # Utilizing waiter to ensure deletion is successful and to keep process alive
        waiter = ec2_client.get_waiter('volume_deleted')
        try:
            waiter.wait(
                VolumeIds=volumes_to_delete,
            )
            print("Total Volumes Deleted:", len(total_deleted))
        except Exception as e:
            print("Error in process with error being: " + str(e))
    else:
     print("No snapshots deleted")

# Simple if statement to output the total deleted and total errors if any
if len(total_errors) > 0:
    print("Total Errors:", len(total_errors))
else:
    print("There were no errors")

# Add functionality for cli argument to delete
if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(description=ARG_HELP, formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        args.add_argument('--delete','-d', dest='delete', action='store_true', help="Use to delete Volumes")
        args = args.parse_args()
        # Launch delete function
        delete(args)
    except KeyboardInterrupt:
        print("\n[!] Key Interrupt Detected...\n\n")
        exit(1)
    exit(0)
