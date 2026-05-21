from src.models import ModelRegistry

def main():
    registry = ModelRegistry()
    model = ApprovedModel('Claude', 'Large Language Model')
    registry.add_approved_model(model)
    approved_models = registry.get_approved_models()
    print(approved_models)

if __name__ == '__main__':
    main()