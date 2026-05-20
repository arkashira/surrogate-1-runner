def load_config():
    import yaml
    with open('/opt/axentx/surrogate-1/config/surrogate-1.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config