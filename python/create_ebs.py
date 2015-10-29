import boto.ec2
import time
import argparse

""" Creates an EBS volume of the specified size in the specified AZ
    and attaches it to the specified instance

    Usage:
    python ebs.py --zone 'us-west-2b' --size '20' --instance 'i-abcdefg' --device '/dev/xvdb'
"""
def create_ebs(ec2, size, zone, max_timeout):
    # timer variables
    interval = 5

    # create a volume
    response = ec2.create_volume(size=size, volume_type='gp2', zone=zone)
    print "Created volume {volume}".format(volume=response.id)

    # poll until status is 'available' or timeout
    if response is not None:
        start_time = time.time()
        while ( max_timeout >= (time.time() - start_time) ):
            status = get_ebs_status(ec2, response.id)
            print ' * Status of {0} is {1}'.format(response.id, status)

            if status == 'available':
                print '=================='
                return response.id
            else:
                time.sleep(interval)

        raise Exception('Timed out. Volume {0} is not available after {1} seconds.'.format(response.id, max_timeout))
    return

""" Attach EBS volume to the specified instance
    and monitor until it becomes 'in-use'
"""
def attach_to_instance(ec2, volume_id, instance_id, device, max_timeout):
    interval = 5

    print 'Attaching volume {0} to instance {1}'.format(volume_id, instance_id)
    response = ec2.attach_volume(volume_id, instance_id, device)

    if response:
        start_time = time.time()
        while ( max_timeout >= (time.time() - start_time) ):
            status = get_ebs_status(ec2, volume_id)
            print ' * Status of {0} is {1}'.format(volume_id, status)

            if status == 'in-use':
                print '=================='
                return True
            else:
                time.sleep(interval)

        raise Exception('Timed out. Volume {0} is not in-use after {1} seconds.'.format(response.id, max_timeout))
    return


def get_ebs_status(ec2, volume_id):
    ebs = ec2.get_all_volumes(volume_id)[0]
    return ebs.status


def tag_volume(ec2, volume_id, name):
    tags = { 'Name' : name }
    print 'Tagging {0} with Name={1}...'.format(volume_id, name)

    if ec2.create_tags(volume_id, tags):
        print ' * Done.'
    else:
        print ' * Failed.'

    print '=================='
    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create and attach an EBS volume.')
    parser.add_argument('--zone', required=True)
    parser.add_argument('--size', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--device', required=True)
    parser.add_argument('--tag', required=True)
    args = parser.parse_args()

    region = args.zone[:-1]
    ec2 = boto.ec2.connect_to_region(region)

    # create volume
    vol_id = create_ebs(ec2, args.size, args.zone, 180)

    # attach volume
    attach_to_instance(ec2, vol_id, args.instance, args.device, 180)

    # tag volume
    tag_volume(ec2, vol_id, '{0}-{1}'.format(args.tag, args.device))
