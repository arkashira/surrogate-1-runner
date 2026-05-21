from .gpt4 import GPT4Model

def get_ai_model(model_name, api_key, api_url):
    if model_name == 'gpt4':
        return GPT4Model(api_key, api_url)
    else:
        raise ValueError('Unsupported AI model')