from pathlib import Path

import docker

import docker.errors


# TODO: write tests for testing exception blocks
import os


class DockerWrapper:
    def __init__(self):
        self.lclient = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.client = docker.from_env()
        self.containers = {}

    def start(self, image, name):
        try:
            logs_dir = os.path.join(Path(__file__).parents[1], 'logs')
            volume_mnt = {logs_dir: {'bind': '/app/logs/', 'mode': 'rw'}}
            container = self.client.containers.run(image, detach=True, name=name, auto_remove=True, volumes=volume_mnt)
            self.containers[container.id] = container
            return container.id, False
        except docker.errors.ContainerError as ce:
            return 'docker container error: {}'.format(ce), True
        except docker.errors.ImageNotFound as ie:
            return 'docker image error: {}'.format(ie), True
        except docker.errors.APIError as ae:
            return 'docker API error: {}'.format(ae), True
        except KeyError:
            return 'invalid container id', True

    def stop(self, container_id):
        try:
            self.containers[container_id].stop()
        except docker.errors.APIError as de:
            return 'docker error: {}'.format(de)
        except KeyError:
            return 'invalid container id'

    def ip_address(self, container_id):
        try:
            inspect_dict = self.lclient.inspect_container(container_id)
            return inspect_dict['NetworkSettings']['Networks']['bridge']['IPAddress'], None
        except docker.errors.APIError as de:
            return None, 'docker error: {}'.format(de)
        # TODO: KeyError
