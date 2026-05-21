import os

def list_templates():
    template_dir = 'templates/library'
    templates = [f for f in os.listdir(template_dir) if f.endswith('.yaml')]
    return templates

def apply_template(template_name):
    template_path = os.path.join('templates/library', template_name)
    with open(template_path, 'r') as file:
        template_content = file.read()

    print(f"Template content:\n{template_content}")
    confirmation = input("Do you want to apply this template to surrogate.yaml? (y/n): ").strip().lower()

    if confirmation == 'y':
        with open('surrogate.yaml', 'w') as file:
            file.write(template_content)
        return True
    return False