#!/usr/bin/python
# Get the Instance Puplic IP

from MaltegoTransform import *
import sys
import os
import boto.ec2
from init import load_credentials

creds = load_credentials()
REGION = creds[2]

amazon_id = sys.argv[1]
searchquery = "[Instance:" + amazon_id + "]"

m = MaltegoTransform()

try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
    reservations = conn.get_all_reservations()
    instance_list = []
    for x in range(0, len(reservations)):
        instances = reservations[x].instances
        if str(searchquery) in str(instances):
            instances = reservations[x].instances
            ent = m.addEntity('maltego.IPv4Address', str(instances[0].ip_address))
            ent.addAdditionalFields("PublicIPAddress", "Public IP Address", "strict", str(instances[0].ip_address))
            m.addUIMessage("Completed")
        else:
            pass
    else:
        m.addUIMessage("Completed")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()
