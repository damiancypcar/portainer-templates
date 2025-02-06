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

        # Filter out lines that start with "# description:" or "# logo:"
        filtered_lines = [
            line for line in lines if not (line.strip().startswith("# description:") or line.strip().startswith("# logo:"))
        ]

        compose_content = ''.join(filtered_lines)

        with open(docker_compose_file, 'r', encoding='utf-8') as file:
            docker_compose = yaml.safe_load(file)

        filename = os.path.basename(docker_compose_file)

        # Get the name of the first service
        service_name = next(iter(docker_compose.get('services', {})), None)

        if service_name:  # If there's at least one service
            template_service = {
                "title": service_name,
                "description": description,
                "note": f"Generated from {filename}",
                "logo": logo,
                "categories": ["Custom"],
                "platform": "linux",
                "type": 3,
                "repository": {
                    "url": "https://github.com/damiancypcar/portainer-templates",
                    "stackfile": f"compose_files/{filename}"
                }
            }

            # Add the processed template service to the main template
            template['templates'].append(template_service)
        else:
            print(f"No services found in {filename}. Skipping this file.")

    # Write the final template to a JSON file with Unix-style line endings
    with open(template_file, 'w', encoding='utf-8', newline='') as file:
        json.dump(template, file, indent=4)

# Get all docker-compose files from the compose_files directory
compose_files_directory = 'compose_files'
docker_compose_files = [os.path.join(compose_files_directory, f) for f in os.listdir(compose_files_directory) if f.endswith('.yml') or f.endswith('.yaml')]

# Generate the templates.json file
docker_compose_to_template(docker_compose_files, 'templates.json')
