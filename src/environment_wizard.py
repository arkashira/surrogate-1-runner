import os
import json
from flask import Blueprint, render_template, request, redirect, url_for
from .aws_services import create_aws_simulation

environment_wizard = Blueprint('environment_wizard', __name__)

@environment_wizard.route('/environment_wizard', methods=['GET', 'POST'])
def create_environment():
    if request.method == 'POST':
        environment_config = {
            'region': request.form['region'],
            'services': request.form.getlist('services'),
            'vpc_config': {
                'cidr': request.form['vpc_cidr'],
                'subnets': request.form.getlist('subnets')
            }
        }

        # Save config to a temporary file
        temp_config_path = '/tmp/environment_config.json'
        with open(temp_config_path, 'w') as config_file:
            json.dump(environment_config, config_file)

        # Create AWS simulation
        create_aws_simulation(temp_config_path)

        # Clean up
        os.remove(temp_config_path)

        return redirect(url_for('environment_wizard.environment_created'))

    return render_template('environment_wizard.html')

@environment_wizard.route('/environment_created')
def environment_created():
    return render_template('environment_created.html')