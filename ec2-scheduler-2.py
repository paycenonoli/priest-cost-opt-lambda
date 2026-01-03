import boto3

ec2 = boto3.client("ec2")

def lambda_handler(event, context):
    filters = [
        {"Name": "tag:Environment", "Values": ["dev"]},
        {"Name": "tag:AutoSchedule", "Values": ["true"]},
        {"Name": "instance-state-name", "Values": ["stopped"]}
    ]

    response = ec2.describe_instances(Filters=filters)

    instance_ids = [
        instance["InstanceId"]
        for reservation in response["Reservations"]
        for instance in reservation["Instances"]
    ]

    if instance_ids:
        ec2.start_instances(InstanceIds=instance_ids)
        print(f"Started instances: {instance_ids}")
    else:
        print("No stopped dev instances found.")

