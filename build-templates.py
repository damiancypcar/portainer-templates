import os
import json
import yaml

def docker_compose_to_template(docker_compose_files, template_file):
    template = {
        "version": "2",
        "templates": []
    }

    for docker_compose_file in docker_compose_files:
        with open(docker_compose_file, 'r') as file:
            docker_compose = yaml.safe_load(file)

        for service_name, service in docker_compose['services'].items():
            template_service = {
                "type": 1,
                "title": service_name,
                "description": f"Template for {service_name}",
                "note": "",
                "categories": [],
                "platform": "linux",
                "logo": "",
                "repository": "",
                "network": {
                    "name": service.get('networks', {}).get('default', {}).get('name', 'bridge'),
                    "driver": service.get('networks', {}).get('default', {}).get('driver', 'bridge')
                },
                "env": [],
                "volumes": [],
                "ports": []
            }

            for env_var in service.get('environment', []):
                name, value = env_var.split('=', 1)
                template_service['env'].append({
                    "name": name,
                    "label": name,
                    "default": value
                })

            for volume in service.get('volumes', []):
                template_service['volumes'].append({
                    "container": volume.split(':')[1],
                    "bind": volume.split(':')[0]
                })

            for port in service.get('ports', []):
                template_service['ports'].append({
                    "containerPort": port.split(':')[1],
                    "hostPort": port.split(':')[0]
                })

            template['templates'].append(template_service)

    with open(template_file, 'w') as file:
        json.dump(template, file, indent=4)

# Get all docker-compose files from the compose_files directory
compose_files_directory = 'compose_files'
docker_compose_files = [os.path.join(compose_files_directory, f) for f in os.listdir(compose_files_directory) if f.endswith('.yml') or f.endswith('.yaml')]

# Generate the template.json file
docker_compose_to_template(docker_compose_files, 'template.json')

