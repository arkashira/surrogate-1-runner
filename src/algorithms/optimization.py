
import boto3
import json
from datetime import datetime, timedelta

ec2 = boto3.resource('ec2')
reservations = ec2.reservations.filter(
    Filters=[{'Name': 'tag:Environment', 'Values': ['production']}]
)

recommendations = []

for reservation in reservations:
    for instance in reservation.instances:
        instance_id = instance.id
        instance_type = instance.instance_type
        current_usage_price = instance.current_usage_price

        similar_instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:Environment', 'Values': ['production']},
                {'Name': 'instance-type', 'Values': [instance_type]},
                {'Name': 'state.name', 'Values': ['running']},
                {'Name': 'instance-id', 'Values': [instance_id]},
                {'Name': 'availability-zone', 'Values': [instance.placement['AvailabilityZone']]}
            ]
        )
        similar_instances_count = len(list(similar_instances))

        if similar_instances_count > 1:
            recommendations.append(f"Consider consolidating {instance_type} instances ({instance_id}). There are {similar_instances_count} similar instances running in the same availability zone.")

        reserved_instances = ec2.reserved_instances.filter(
            Filters=[
                {'Name': 'tag:Environment', 'Values': ['production']},
                {'Name': 'instance-type', 'Values': [instance_type]},
                {'Name': 'availability-zone', 'Values': [instance.placement['AvailabilityZone']]}
            ]
        )
        reserved_instances_count = len(list(reserved_instances))

        if reserved_instances_count > 0:
            reserved_instance = reserved_instances[0]
            reserved_instance_price = reserved_instance.price_hour

            if reserved_instance_price < current_usage_price:
                recommendations.append(f"Consider using Reserved Instance for {instance_type} instances ({instance_id}). The Reserved Instance price is {reserved_instance_price} while the current usage price is {current_usage_price}.")

recommendations_json = json.dumps(recommendations)

# Save recommendations to a file for display on the dashboard
with open('/opt/axentx/surrogate-1/recommendations.json', 'w') as f:
    f.write(recommendations_json)