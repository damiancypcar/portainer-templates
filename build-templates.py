import os
import json
import yaml

def docker_compose_to_template(docker_compose_files, template_file):
    template = {
        "version": "2",
        "templates": []
    }

    for docker_compose_file in docker_compose_files:
        with open(docker_compose_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        description = ""
        logo = ""

        # Process lines to extract description and logo if available
        for line in lines:
            if line.strip().startswith("# description:"):
                description = line.strip().split(":", 1)[1].strip().strip("'\"")  # Extract description
            elif line.strip().startswith("# logo:"):
                logo = line.strip().split(":", 1)[1].strip().strip("'\"")  # Extract logo URL

        # Filter out lines that starts with "# description:" or "# logo:"
        filtered_lines = [
            line for line in lines if not (line.strip().startswith("# description:") or line.strip().startswith("# logo:"))
        ]

        compose_content = ''.join(filtered_lines)

        with open(docker_compose_file, 'r', encoding='utf-8') as file:
            docker_compose = yaml.safe_load(file)

        filename = os.path.basename(docker_compose_file)

        for service_name, service in docker_compose.get('services', {}).items():
            template_service = {
                "title": service_name,
                "description": description,
                "note": f"Generated from {filename}",
                "logo": logo,
                "categories": ["Custom"],
                "platform": "linux",
                "type": 1,
                "repository": {
                    "stackfile": compose_content  # Add the entire content of the Docker Compose file here
                },
                "network": {
                    "name": service.get('networks', {}).get('default', {}).get('name', 'bridge'),
                    "driver": service.get('networks', {}).get('default', {}).get('driver', 'bridge')
                },
                "env": [],
                "volumes": [],
                "ports": []
            }

            # Process environment variables
            for env_var in service.get('environment', {}):
                if isinstance(env_var, str) and '=' in env_var:
                    name, value = env_var.split('=', 1)
                elif isinstance(env_var, dict):
                    name, value = list(env_var.items())[0]
                else:
                    continue
                template_service['env'].append({
                    "name": name,
                    "label": name,
                    "default": value
                })

            # Process volumes
            for volume in service.get('volumes', []):
                parts = volume.split(':')
                if len(parts) == 2:
                    template_service['volumes'].append({
                        "container": parts[1],
                        "bind": parts[0]
                    })

            # Process ports
            for port in service.get('ports', []):
                parts = port.split(':')
                if len(parts) == 2:
                    template_service['ports'].append({
                        "containerPort": parts[1],
                        "hostPort": parts[0]
                    })

            # Add the processed template service to the main template
            template['templates'].append(template_service)

    # Write the final template to a JSON file with Unix-style line endings
    with open(template_file, 'w', encoding='utf-8', newline='') as file:
        json.dump(template, file, indent=4)

# Get all docker-compose files from the compose_files directory
compose_files_directory = 'compose_files'
docker_compose_files = [os.path.join(compose_files_directory, f) for f in os.listdir(compose_files_directory) if f.endswith('.yml') or f.endswith('.yaml')]

# Generate the templates.json file
docker_compose_to_template(docker_compose_files, 'templates.json')
