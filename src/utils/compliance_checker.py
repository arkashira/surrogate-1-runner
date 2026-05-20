def check_compliance(data):
    compliance_status = {
        'is_compliant': True,
        'non_compliant_fields': []
    }

    if not isinstance(data, dict):
        return compliance_status

    for key, value in data.items():
        if isinstance(value, dict):
            nested_status = check_compliance(value)
            if not nested_status['is_compliant']:
                compliance_status['is_compliant'] = False
                compliance_status['non_compliant_fields'].extend(nested_status['non_compliant_fields'])
        elif isinstance(value, str):
            if re.search(r'\d{3}-\d{2}-\d{4}', value):
                compliance_status['is_compliant'] = False
                compliance_status['non_compliant_fields'].append(key)
            elif re.search(r'\b\d{16}\b', value):
                compliance_status['is_compliant'] = False
                compliance_status['non_compliant_fields'].append(key)

    return compliance_status