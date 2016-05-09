#!/usr/bin/env python

"""

Ansible dynamic inventory that gets the docker-machine host and it's
variables into the inventory to the 'docker-host' group.

Example Usage:

> eval "$(docker-machine env MACHINE_NAME)"
$ ansible-playbook playbook.yml -i docker-machine.py

Debug:

python docker-machine.py

"""

import os
import argparse
import subprocess

try:
    import json
except ImportError:
    import simplejson as json


"""
    Gets information about a docker machine.
    docker-machine host
"""
def getDockerMachineInfo(machineName, format):
    return subprocess.check_output([
        "docker-machine",
        "inspect",
        "-f",
        format,
        machineName ]).strip()


"""
    Gets all available docker machines.
    Returning the list of available docker machines
"""
def getAllDockerMachines(machineName, format):
    return subprocess.check_output([
        "docker-machine",
        "ls",
        "-q" ]).strip()


"""
    Get the docker machine inventory group.
    Returns the docker host group
"""
def getAnsibleDockerInventoryGroup(dmName):

    return {
        "hosts": ["localhost"],
        "vars": {

            # at the moment docker-machine is always using this port
            "docker_host_url": "tcp://{}:2376".format(
                getDockerMachineInfo(dmName, "{{.Driver.IPAddress}}")),

            "docker_host_cert_path": getDockerMachineInfo(dmName, "{{.HostOptions.AuthOptions.StorePath}}"),

            "ansible_connection": "local"
        }
    }


# get the current docker machine name
docker_machine_name = os.environ['DOCKER_MACHINE_NAME']
if docker_machine_name is None:
    raise Exception('Missing DOCKER_MACHINE_NAME environment variable')

# add the docker-machine to the inventory
json_data = {
    "docker-host": getAnsibleDockerInventoryGroup(docker_machine_name),
    "local": {
        "hosts": ["localhost"],
        "vars": { "ansible_connection": "local" }
    }
}

print json.dumps(json_data, indent=4)
