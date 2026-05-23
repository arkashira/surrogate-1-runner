def validate_hardening_payload(data):
    if not isinstance(data, dict):
        return False

    if 'vm_ids' not in data or not isinstance(data['vm_ids'], list):
        return False

    if 'policy_version' in data and not isinstance(data['policy_version'], str):
        return False

    return True